import { useState } from 'react';
import {
  BookOpen,
  CheckCircle2,
  Lightbulb,
  AlertTriangle,
  ArrowRight,
  BookmarkCheck,
  Compass,
  GraduationCap,
  Sparkles
} from 'lucide-react';
import Button from '../common/Button';
import Card from '../common/Card';
import {
  PERCENTAGE_PDF_EN,
  PERCENTAGE_PDF_TA,
  type PercentagePdfLesson
} from '../../data/percentageLessonData';
import {
  RATIO_PDF_EN,
  RATIO_PDF_TA,
  type LessonPdfData
} from '../../data/ratioLessonData';
import {
  TIME_AND_WORK_PDF_EN,
  TIME_AND_WORK_PDF_TA
} from '../../data/timeAndWorkLessonData';
import {
  AREA_AND_VOLUME_PDF_EN,
  AREA_AND_VOLUME_PDF_TA
} from '../../data/areaAndVolumeLessonData';
import {
  LOGICAL_REASONING_PDF_EN,
  LOGICAL_REASONING_PDF_TA
} from '../../data/logicalReasoningLessonData';
import {
  NUMBER_SERIES_PDF_EN,
  NUMBER_SERIES_PDF_TA
} from '../../data/numberSeriesLessonData';
import {
  SIMPLIFICATION_PDF_EN,
  SIMPLIFICATION_PDF_TA
} from '../../data/simplificationLessonData';
import {
  PUZZLES_PDF_EN,
  PUZZLES_PDF_TA
} from '../../data/puzzlesLessonData';
import type { AssessmentItem } from '../../types';

interface Props {
  assessments: AssessmentItem[];
  courseTitle: string;
  courseSlug?: string;
  language?: 'en' | 'ta';
  onGoToPractice?: () => void;
}

export default function CourseLearnSection({ assessments, courseTitle, courseSlug, language = 'en', onGoToPractice }: Props) {
  const isPuzzles = Boolean(
    (courseSlug && courseSlug.includes('puzzle')) ||
    (courseTitle && (courseTitle.toLowerCase().includes('puzzle') || courseTitle.includes('புதிர்')))
  );

  const isSimplification = Boolean(
    (courseSlug && courseSlug.includes('simplification')) ||
    (courseTitle && (courseTitle.toLowerCase().includes('simplification') || courseTitle.includes('சுருக்குதல்')))
  );

  const isNumberSeries = Boolean(
    (courseSlug && (courseSlug.includes('number') || courseSlug.includes('series'))) ||
    (courseTitle && (courseTitle.toLowerCase().includes('number') || courseTitle.toLowerCase().includes('series') || courseTitle.includes('எண்') || courseTitle.includes('தொடர்')))
  );

  const isLogicalReasoning = Boolean(
    (courseSlug && (courseSlug.includes('logical') || courseSlug.includes('reasoning'))) ||
    (courseTitle && (courseTitle.toLowerCase().includes('logical') || courseTitle.toLowerCase().includes('reasoning') || courseTitle.includes('தருக்க') || courseTitle.includes('காரணவியல்')))
  );

  const isAreaVolume = Boolean(
    (courseSlug && (courseSlug.includes('area') || courseSlug.includes('volume'))) ||
    (courseTitle && (courseTitle.toLowerCase().includes('area') || courseTitle.toLowerCase().includes('volume') || courseTitle.includes('பரப்பளவு') || courseTitle.includes('கன அளவு')))
  );

  const isTimeWork = Boolean(
    (courseSlug && (courseSlug.includes('time') || courseSlug.includes('work'))) ||
    (courseTitle && (courseTitle.toLowerCase().includes('time') || courseTitle.includes('காலம்') || courseTitle.includes('வேலை')))
  );

  const isRatio = Boolean(
    (courseSlug && courseSlug.includes('ratio')) ||
    (courseTitle && (courseTitle.toLowerCase().includes('ratio') || courseTitle.includes('விகிதம்')))
  );

  const courseKey = isPuzzles ? 'puzzles' : isSimplification ? 'simplification' : isNumberSeries ? 'numberseries' : isLogicalReasoning ? 'logicalreasoning' : isAreaVolume ? 'areavolume' : isTimeWork ? 'timework' : isRatio ? 'ratio' : 'percentage';
  const storageKey = `exampro_completed_${courseKey}_lesson`;

  const [completed, setCompleted] = useState<boolean>(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      return saved === 'true';
    } catch {
      return false;
    }
  });

  const toggleComplete = () => {
    setCompleted((prev) => {
      const next = !prev;
      try {
        localStorage.setItem(storageKey, String(next));
      } catch { }
      return next;
    });
  };

  const lesson: LessonPdfData | PercentagePdfLesson = isPuzzles
    ? (language === 'ta' ? PUZZLES_PDF_TA : PUZZLES_PDF_EN)
    : isSimplification
    ? (language === 'ta' ? SIMPLIFICATION_PDF_TA : SIMPLIFICATION_PDF_EN)
    : isNumberSeries
    ? (language === 'ta' ? NUMBER_SERIES_PDF_TA : NUMBER_SERIES_PDF_EN)
    : isLogicalReasoning
    ? (language === 'ta' ? LOGICAL_REASONING_PDF_TA : LOGICAL_REASONING_PDF_EN)
    : isAreaVolume
    ? (language === 'ta' ? AREA_AND_VOLUME_PDF_TA : AREA_AND_VOLUME_PDF_EN)
    : isTimeWork
    ? (language === 'ta' ? TIME_AND_WORK_PDF_TA : TIME_AND_WORK_PDF_EN)
    : isRatio
    ? (language === 'ta' ? RATIO_PDF_TA : RATIO_PDF_EN)
    : (language === 'ta' ? PERCENTAGE_PDF_TA : PERCENTAGE_PDF_EN);

  const practiceCount = isPuzzles ? 55 : isSimplification ? 55 : isNumberSeries ? 55 : isLogicalReasoning ? 55 : isAreaVolume ? 55 : isTimeWork ? 55 : isRatio ? 55 : 60;

  return (
    <div className="space-y-6">
      {/* Top Banner / Hero */}
      <div className="relative overflow-hidden rounded-2xl border border-sky-100 bg-gradient-to-br from-sky-50/80 via-white to-sky-100/40 p-5 sm:p-6 shadow-xs">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1 rounded-full bg-sky-600 px-3 py-0.5 text-xs font-semibold text-white shadow-xs">
                <BookOpen className="h-3.5 w-3.5" />
                {lesson.lessonTitle}
              </span>
              <span className="text-xs font-medium text-navy-500">
                {language === 'ta' ? 'அதிகாரப்பூர்வப் பாடக் குறிப்பேடு' : 'Official Curriculum Study Module'}
              </span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-navy tracking-tight">
              {lesson.lessonTitle}
            </h3>
            <p className="text-xs sm:text-sm text-navy-600 max-w-2xl">
              {language === 'ta'
                ? 'TNPSC குரூப் 1, UPSC, SSC மற்றும் வங்கித் தேர்வுகளுக்கான விரிவான கருத்து விளக்கம் மற்றும் தேர்வுக் குறிப்புகள்.'
                : 'Comprehensive theory, exam insights, core concepts, common pitfalls, and strategy tips for competitive examinations.'}
            </p>
          </div>

          <button
            type="button"
            onClick={toggleComplete}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-semibold transition-all shadow-xs shrink-0 ${
              completed
                ? 'bg-mint-600 text-white shadow-mint-600/20'
                : 'bg-white border border-line text-navy-700 hover:bg-navy-50'
            }`}
          >
            <CheckCircle2 className={`h-4 w-4 ${completed ? 'text-white' : 'text-navy-400'}`} />
            <span>{completed ? (language === 'ta' ? 'படித்தேன் ✓' : 'Understood ✓') : (language === 'ta' ? 'படித்ததாகக் குறிக்கவும்' : 'Mark as read')}</span>
          </button>
        </div>
      </div>

      {/* ---------------------------------------------------- */}
      {/* 1. LEARNING OBJECTIVES                                */}
      {/* ---------------------------------------------------- */}
      <section className="rounded-xl border border-line bg-white p-5 shadow-xs transition-shadow hover:shadow-sm">
        <div className="flex items-center gap-2.5 border-b border-line pb-3.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-100 text-sky-800 text-sm font-bold">
            1
          </div>
          <div>
            <h3 className="text-base font-bold text-navy flex items-center gap-2">
              {lesson.objectivesTitle}
            </h3>
            <p className="text-xs text-navy-500 mt-0.5">{lesson.objectivesPreamble}</p>
          </div>
        </div>

        <ol className="mt-4 space-y-2.5 text-xs sm:text-sm text-navy-800">
          {lesson.objectives.map((obj, i) => (
            <li key={i} className="flex items-start gap-3 rounded-lg bg-navy-50/40 p-2.5 border border-line/60">
              <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-sky-700 text-[11px] font-bold text-white">
                {i + 1}
              </span>
              <span className="leading-relaxed font-medium">{obj}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* ---------------------------------------------------- */}
      {/* 2. LESSON OVERVIEW                                    */}
      {/* ---------------------------------------------------- */}
      <section className="rounded-xl border border-line bg-white p-5 shadow-xs transition-shadow hover:shadow-sm">
        <div className="flex items-center gap-2.5 border-b border-line pb-3.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-100 text-sky-800 text-sm font-bold">
            2
          </div>
          <h3 className="text-base font-bold text-navy">
            {lesson.overviewTitle}
          </h3>
        </div>

        <div className="mt-4 rounded-lg bg-navy-50/50 p-4 border border-line/60">
          <p className="text-xs sm:text-sm text-navy-800 leading-relaxed font-normal">
            {lesson.overview}
          </p>
        </div>
      </section>

      {/* ---------------------------------------------------- */}
      {/* 3. CONCEPT EXPLANATION                                */}
      {/* ---------------------------------------------------- */}
      <section className="rounded-xl border border-line bg-white p-5 shadow-xs space-y-6">
        <div className="flex items-center gap-2.5 border-b border-line pb-3.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-100 text-sky-800 text-sm font-bold">
            3
          </div>
          <h3 className="text-base font-bold text-navy">
            {lesson.conceptTitle}
          </h3>
        </div>

        {/* 3.1 Exam Insight */}
        <div className="rounded-lg border border-sky-100 bg-sky-50/40 p-4 space-y-2">
          <div className="flex items-center gap-2 text-sky-900 font-bold text-sm">
            <Compass className="h-4 w-4 text-sky-700" />
            <h4>{lesson.examInsightTitle}</h4>
          </div>
          <p className="text-xs sm:text-sm text-navy-800 leading-relaxed font-normal pl-6">
            {lesson.examInsight}
          </p>
        </div>

        {/* 3.2 Core Concepts */}
        <div className="rounded-lg border border-line bg-white p-4 space-y-3">
          <div className="flex items-center gap-2 text-navy font-bold text-sm border-b border-line/60 pb-2">
            <Lightbulb className="h-4 w-4 text-amber-500" />
            <h4>{lesson.coreConceptsTitle}</h4>
          </div>
          <p className="text-xs sm:text-sm font-medium text-navy-700">
            {lesson.coreConceptsIntro}
          </p>
          <ul className="space-y-2 pl-2">
            {lesson.coreConcepts.map((pt, i) => (
              <li key={i} className="flex items-start gap-2.5 text-xs sm:text-sm text-navy-800 leading-relaxed">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-sky-600" />
                <span>{pt}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* 3.3 Common Mistakes */}
        <div className="rounded-lg border border-rose-100 bg-rose-50/30 p-4 space-y-3">
          <div className="flex items-center gap-2 text-rose-900 font-bold text-sm border-b border-rose-100 pb-2">
            <AlertTriangle className="h-4 w-4 text-rose-600" />
            <h4>{lesson.commonMistakesTitle}</h4>
          </div>
          <ul className="space-y-2 pl-2">
            {lesson.commonMistakes.map((mis, i) => (
              <li key={i} className="flex items-start gap-2.5 text-xs sm:text-sm text-navy-800 leading-relaxed">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-rose-500" />
                <span>{mis}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* 3.4 Examination Tips */}
        <div className="rounded-lg border border-mint-200 bg-mint-50/30 p-4 space-y-3">
          <div className="flex items-center gap-2 text-mint-900 font-bold text-sm border-b border-mint-200 pb-2">
            <Sparkles className="h-4 w-4 text-mint-600" />
            <h4>{lesson.examTipsTitle}</h4>
          </div>
          <ul className="space-y-2 pl-2">
            {lesson.examTips.map((tip, i) => (
              <li key={i} className="flex items-start gap-2.5 text-xs sm:text-sm text-navy-800 leading-relaxed">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-mint-600" />
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Bottom Practice CTA */}
      {onGoToPractice && (
        <div className="rounded-xl border border-amber-200 bg-gradient-to-r from-amber-50 to-amber-100/40 p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="space-y-0.5 text-center sm:text-left">
            <h4 className="text-sm font-bold text-amber-900">
              {language === 'ta' ? 'கருத்துகளைப் படித்து முடித்தீர்களா?' : 'Ready to test your understanding?'}
            </h4>
            <p className="text-xs text-amber-800">
              {language === 'ta'
                ? `${practiceCount} பயிற்சிக் கணக்குகளை (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனே தொடங்கவும்.`
                : `Move to step 2 to solve ${practiceCount} untimed practice questions with instant solutions.`}
            </p>
          </div>
          <Button onClick={onGoToPractice} icon={<ArrowRight className="h-4 w-4" />}>
            {language === 'ta' ? '2. பயிற்சிக்குச் செல்க' : 'Proceed to Practice'}
          </Button>
        </div>
      )}
    </div>
  );
}
