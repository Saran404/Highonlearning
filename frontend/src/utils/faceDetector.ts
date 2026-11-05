/**
 * Client-side Face & Person Presence Detection Engine for Exam Proctoring.
 *
 * Utilizes hardware-accelerated W3C Shape Detection API (window.FaceDetector) where available
 * (Chromium / Chrome / Edge / Android Chrome), with a fallback canvas-based
 * skin-chrominance and facial variance detector for Safari, Firefox, and iOS.
 */

// Reusable offscreen canvas to avoid garbage collection and memory churn
let cachedCanvas: HTMLCanvasElement | null = null;
let cachedCtx: CanvasRenderingContext2D | null = null;

// Native FaceDetector instance cache
let nativeDetector: any = null;
let nativeDetectorChecked = false;

export interface DetectionResult {
  visible: boolean;
  confidence: number;
  method: 'native' | 'canvas' | 'unready';
  reason?: string;
}

/**
 * Checks whether a human face/person is visible in the provided <video> element.
 */
export async function detectPersonInVideo(video: HTMLVideoElement | null): Promise<DetectionResult> {
  if (
    !video ||
    video.readyState < 2 ||
    video.paused ||
    video.videoWidth === 0 ||
    video.videoHeight === 0
  ) {
    // Stream not ready or video not playing yet; assume visible during warmup
    return { visible: true, confidence: 1, method: 'unready' };
  }

  // 1. Primary: Native Browser FaceDetector (Chrome, Edge, Android Chrome, WebView, Opera)
  if (typeof window !== 'undefined' && 'FaceDetector' in window) {
    try {
      if (!nativeDetector && !nativeDetectorChecked) {
        nativeDetectorChecked = true;
        // @ts-ignore
        nativeDetector = new window.FaceDetector({ fastMode: true, maxDetectedFaces: 2 });
      }

      if (nativeDetector) {
        const faces = await nativeDetector.detect(video);
        if (Array.isArray(faces)) {
          if (faces.length > 0) {
            return { visible: true, confidence: 0.98, method: 'native' };
          }
          return { visible: false, confidence: 0.95, method: 'native', reason: 'NO_FACE_DETECTED' };
        }
      }
    } catch {
      // If native detector fails or throws (e.g. security origin), fall through to canvas analysis
    }
  }

  // 2. Fallback: High-Performance Canvas Person & Face Presence Analyzer
  const sampleW = 160;
  const sampleH = 120;

  if (!cachedCanvas) {
    cachedCanvas = document.createElement('canvas');
    cachedCanvas.width = sampleW;
    cachedCanvas.height = sampleH;
    cachedCtx = cachedCanvas.getContext('2d', { willReadFrequently: true });
  }

  if (!cachedCtx) {
    return { visible: true, confidence: 0.5, method: 'canvas' };
  }

  try {
    cachedCtx.drawImage(video, 0, 0, sampleW, sampleH);
    const imgData = cachedCtx.getImageData(0, 0, sampleW, sampleH);
    const data = imgData.data;
    const totalPixels = sampleW * sampleH;

    // Check A: Darkness & Flat Contrast (Camera Covered / Blocked Lens / Pitch Black)
    let totalLuma = 0;
    let totalLumaSq = 0;
    for (let i = 0; i < data.length; i += 4) {
      const y = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
      totalLuma += y;
      totalLumaSq += y * y;
    }

    const avgLuma = totalLuma / totalPixels;
    const lumaVariance = totalLumaSq / totalPixels - avgLuma * avgLuma;

    // Lens covered or pitch dark
    if (avgLuma < 18) {
      return { visible: false, confidence: 0.9, method: 'canvas', reason: 'CAMERA_COVERED_DARK' };
    }
    // Pure solid color (e.g., lens taped or pointing at blinding light with 0 contrast)
    if (lumaVariance < 8) {
      return { visible: false, confidence: 0.85, method: 'canvas', reason: 'LENS_COVERED_FLAT' };
    }

    // Check B: Face Region Analysis (Center 60% of frame where person sits)
    const minX = Math.floor(sampleW * 0.2); // 32
    const maxX = Math.floor(sampleW * 0.8); // 128
    const minY = Math.floor(sampleH * 0.12); // 14
    const maxY = Math.floor(sampleH * 0.85); // 102

    const roiPixels = (maxX - minX) * (maxY - minY);
    let skinPixels = 0;
    let roiLuma = 0;
    let roiLumaSq = 0;

    for (let y = minY; y < maxY; y++) {
      for (let x = minX; x < maxX; x++) {
        const idx = (y * sampleW + x) * 4;
        const r = data[idx];
        const g = data[idx + 1];
        const b = data[idx + 2];

        // Standard ITU-R BT.601 RGB -> YCbCr conversion
        const Y = 0.299 * r + 0.587 * g + 0.114 * b;
        const Cb = -0.168736 * r - 0.331264 * g + 0.5 * b + 128;
        const Cr = 0.5 * r - 0.418688 * g - 0.081312 * b + 128;

        roiLuma += Y;
        roiLumaSq += Y * Y;

        // Universal Human Skin Chrominance Model (covers all global skin tones)
        const isSkin =
          Cb >= 77 &&
          Cb <= 132 &&
          Cr >= 130 &&
          Cr <= 178 &&
          Y >= 30 &&
          Y <= 235 &&
          r > g &&
          r > b &&
          r - g >= 6;

        if (isSkin) {
          skinPixels++;
        }
      }
    }

    const skinRatio = skinPixels / roiPixels;
    const roiAvgLuma = roiLuma / roiPixels;
    const roiVariance = roiLumaSq / roiPixels - roiAvgLuma * roiAvgLuma;

    // A person in the camera frame exhibits:
    // 1. Skin-tone cluster in the center (> 3.5% of ROI)
    // 2. Facial features contrast (eyes, lips, shadows, hair: variance > 12)
    if (skinRatio >= 0.035 && roiVariance >= 12) {
      return { visible: true, confidence: Math.min(1, skinRatio * 5), method: 'canvas' };
    }

    // In low light or silhouetted conditions: person presence with higher contrast
    if (skinRatio >= 0.02 && roiVariance >= 35) {
      return { visible: true, confidence: 0.75, method: 'canvas' };
    }

    return { visible: false, confidence: 0.85, method: 'canvas', reason: 'NO_PERSON_IN_FRAME' };
  } catch {
    // If context draw fails for any reason, don't block
    return { visible: true, confidence: 0.5, method: 'canvas' };
  }
}

/**
 * Plays a short, gentle warning chime using Web Audio API to alert the student.
 * Safe to call even if audio is muted or disallowed.
 */
export function playWarningChime(): void {
  try {
    const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = 'sine';
    const now = ctx.currentTime;
    osc.frequency.setValueAtTime(587.33, now); // D5
    osc.frequency.setValueAtTime(440.0, now + 0.15); // A4

    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

    osc.start(now);
    osc.stop(now + 0.4);
  } catch {
    // Silently continue if Web Audio is restricted
  }
}
