/** Exact Area and Volume Lesson Theory extracted directly from AreaandVolumeenglish and AreaandVolumetamil PDFs. */
import type { LessonPdfData } from './ratioLessonData';

export const AREA_AND_VOLUME_PDF_EN: LessonPdfData = {
  lessonTitle: '4. Area and Volume',
  objectivesTitle: '1. Learning Objectives',
  objectivesPreamble: 'The learner will be able to:',
  objectives: [
    'Calculate the area of plane figures (rectangle, square, triangle, circle, trapezium) and the volume and surface area of solids (cube, cuboid, cylinder, cone, sphere, hemisphere).',
    'Apply the scaling relationship between linear, area, and volume ratios.',
    'Solve composite-figure, melting-and-recasting, and practical cost-based (fencing, whitewashing, fabric) problems.',
    'Solve multi-step, competitive-examination-standard questions on Area and Volume efficiently, using Task Strategies, Attention Control, Self-Monitoring, and Self-Evaluation & Reflection.'
  ],
  overviewTitle: '2. Lesson Overview',
  overview:
    'Area and Volume is a core Analytical Skills topic in TNPSC Group 1 and allied competitive examinations, testing a candidate’s ability to interpret geometrical information, analyse spatial relationships, and apply appropriate formulas to practical and examination-oriented problems. This lesson emphasises higher-order, multi-step problem solving – composite figures, melting-and-recasting of solids, scale-factor ratios, and cost-based applications – rather than simple one-step formula recall.',
  conceptTitle: '3. Concept Explanation',
  examInsightTitle: '3.1 Exam Insight',
  examInsight:
    'In TNPSC Group 1 and similar competitive examinations, Area and Volume questions rarely stop at “find the area of a rectangle.” They typically combine two or more conditions – a path or border around a field, melting one solid into another shape, a scale-factor ratio, or a cost calculation – and require the candidate to set up a relationship before solving. This lesson’s questions are built to that standard: each one requires at least two reasoning steps, not a single plug-in.',
  coreConceptsTitle: '3.2 Core Concepts',
  coreConceptsIntro:
    'Area measures a plane region; volume measures the space occupied by a solid; surface area measures the total exposed surface of a solid. In competitive examinations, learners should be proficient in:',
  coreConcepts: [
    'Standard area formulas: rectangle (l×b), square (a²), triangle (½×base×height), circle (πr²), trapezium (½×(a+b)×h).',
    'Standard volume formulas: cube (a³), cuboid (l×b×h), cylinder (πr²h), cone (⅓πr²h), sphere (4/3πr³), hemisphere (2/3πr³).',
    'Curved and total surface area formulas for cylinder, cone, sphere, and hemisphere.',
    'The scaling rule: if linear dimensions scale by a factor k, area scales by k² and volume scales by k³.',
    'Solving composite-figure problems (a path around a field, an embankment around a well) by subtracting or adding known regions.',
    'Melting-and-recasting problems, where the volume of the original solid equals the volume of the new solid(s).',
    'Practical applications: cost of fencing (perimeter-based), cost of whitewashing or painting (surface-area-based), and fabric required for a conical tent (curved surface area).'
  ],
  commonMistakesTitle: '3.3 Common Mistakes',
  commonMistakes: [
    'Using the diameter in place of the radius in area or volume formulas.',
    'Confusing curved surface area (CSA) with total surface area (TSA) for cylinders, cones, and hemispheres.',
    'Forgetting that area scales as the square, and volume as the cube, of the linear scale factor – not the same factor as length.',
    'In composite-figure problems, adding instead of subtracting the inner region, or vice versa.',
    'In melting-and-recasting problems, equating surface areas instead of volumes.',
    'Forgetting to convert units (e.g., cm to m) before adding or comparing quantities.'
  ],
  examTipsTitle: '3.4 Examination Tips',
  examTips: [
    'Before calculating, restate exactly what is being asked – area, volume, CSA, or TSA – since these are frequently confused under time pressure.',
    'For scale-factor problems, apply k² for area ratio and k³ for volume ratio directly, without recomputing each figure’s dimensions.',
    'In composite-figure (path/embankment) problems, always compute the outer and inner regions separately before subtracting.',
    'In melting-and-recasting problems, equate the volumes of the original and new solid(s), and solve for the unknown dimension.',
    'Use π = 22/7 when the radius is a multiple of 7 (or leads to a denominator of 7) for exact answers; otherwise use π ≈ 3.14.'
  ]
};

export const AREA_AND_VOLUME_PDF_TA: LessonPdfData = {
  lessonTitle: '4. பரப்பளவு மற்றும் கன அளவு',
  objectivesTitle: '1. கற்றல் நோக்கங்கள்',
  objectivesPreamble: 'இப்பாடத்தை நிறைவு செய்த பின் கற்போர் பின்வருவனவற்றைச் செய்ய இயலும்:',
  objectives: [
    'தள உருவங்களின் (செவ்வகம், சதுரம், முக்கோணம், வட்டம், சரிவகம்) பரப்பளவையும், திண்ம உருவங்களின் (கனசதுரம், கனச்செவ்வகம், உருளை, கூம்பு, கோளம், அரைக்கோளம்) கன அளவு மற்றும் புறப்பரப்பையும் கணக்கிடுதல்.',
    'நீள, பரப்பு, கன அளவு விகிதங்களுக்கு இடையிலான அளவுமாற்றத் தொடர்பைப் பயன்படுத்துதல்.',
    'கூட்டு உருவம், உருக்கி மறுவார்ப்பு, நடைமுறைச் செலவு சார்ந்த (வேலி அமைத்தல், வெள்ளையடித்தல், துணி) கணக்குகளைத் தீர்த்தல்.',
    'பணி உத்திகள், கவனக் கட்டுப்பாடு, சுயக் கண்காணிப்பு, சுய மதிப்பீடு மற்றும் சிந்தனை ஆகியவற்றைப் பயன்படுத்தி, போட்டித் தேர்வுத் தரத்திலான பல படிநிலைப் பரப்பளவு மற்றும் கன அளவு வினாக்களைத் திறம்படத் தீர்த்தல்.'
  ],
  overviewTitle: '2. பாடக் கண்ணோட்டம்',
  overview:
    'பரப்பளவு மற்றும் கன அளவு என்பது TNPSC குரூப் 1 மற்றும் அது சார்ந்த போட்டித் தேர்வுகளில் ஒரு முக்கியப் பகுப்பாய்வுத் திறன் தலைப்பாகும். வடிவியல் தகவல்களைப் புரிந்துகொள்ளுதல், இடஞ்சார்ந்த தொடர்புகளைப் பகுப்பாய்தல், நடைமுறை மற்றும் தேர்வு நோக்கிலான கணக்குகளுக்குப் பொருத்தமான சூத்திரங்களைப் பயன்படுத்துதல் ஆகிய தேர்வரின் திறன்களை இது சோதிக்கிறது. இப்பாடம் எளிய ஒருபடி சூத்திர நினைவுகூர்தலுக்குப் பதிலாக, உயர்நிலை, பல படிநிலைச் சிக்கல் தீர்த்தலுக்கு – கூட்டு உருவங்கள், திண்மங்களை உருக்கி மறுவார்த்தல், அளவுமாற்றக் காரணி விகிதங்கள், செலவு சார்ந்த பயன்பாடுகள் – முக்கியத்துவம் அளிக்கிறது.',
  conceptTitle: '3. கருத்து விளக்கம்',
  examInsightTitle: '3.1 தேர்வு நோக்கு',
  examInsight:
    'TNPSC குரூப் 1 மற்றும் இதுபோன்ற போட்டித் தேர்வுகளில், பரப்பளவு மற்றும் கன அளவு வினாக்கள் “ஒரு செவ்வகத்தின் பரப்பளவைக் காண்க” என்பதோடு நிற்பது அரிது. அவை பொதுவாக இரண்டு அல்லது அதற்கு மேற்பட்ட நிபந்தனைகளை – ஒரு வயலைச் சுற்றியுள்ள பாதை அல்லது எல்லை, ஒரு திண்மத்தை உருக்கி வேறு வடிவமாக்குதல், அளவுமாற்றக் காரணி விகிதம், அல்லது செலவுக் கணக்கீடு – இணைக்கின்றன; தீர்ப்பதற்கு முன் தேர்வர் ஒரு தொடர்பை அமைக்க வேண்டியுள்ளது. இப்பாடத்தின் வினாக்கள் அந்த தரத்தில் அமைக்கப்பட்டுள்ளன: ஒவ்வொரு வினாவும் ஒரே ஒரு மதிப்பைப் பிரதியிடுவதாக இல்லாமல், குறைந்தது இரண்டு தர்க்கப் படிநிலைகளைக் கோருகிறது.',
  coreConceptsTitle: '3.2 அடிப்படைக் கருத்துகள்',
  coreConceptsIntro:
    'பரப்பளவு ஒரு தளப் பகுதியை அளக்கிறது; கன அளவு ஒரு திண்மம் அடைத்துக்கொள்ளும் இடத்தை அளக்கிறது; புறப்பரப்பு ஒரு திண்மத்தின் மொத்த வெளிப்புறப் பரப்பை அளக்கிறது. போட்டித் தேர்வுகளில் கற்போர் பின்வருவனவற்றில் தேர்ச்சி பெற்றிருக்க வேண்டும்:',
  coreConcepts: [
    'அடிப்படைப் பரப்பளவுச் சூத்திரங்கள்: செவ்வகம் (l×b), சதுரம் (a²), முக்கோணம் (½×அடிப்பக்கம்×உயரம்), வட்டம் (πr²), சரிவகம் (½×(a+b)×h).',
    'அடிப்படைக் கன அளவுச் சூத்திரங்கள்: கனசதுரம் (a³), கனச்செவ்வகம் (l×b×h), உருளை (πr²h), கூம்பு (⅓πr²h), கோளம் (4/3πr³), அரைக்கோளம் (2/3πr³).',
    'உருளை, கூம்பு, கோளம், அரைக்கோளம் ஆகியவற்றின் வளைபரப்பு மற்றும் மொத்தப் புறப்பரப்புச் சூத்திரங்கள்.',
    'அளவுமாற்ற விதி: நீள அளவுகள் k என்ற காரணியால் மாறினால், பரப்பளவு k² ஆலும் கன அளவு k³ ஆலும் மாறுகின்றன.',
    'தெரிந்த பகுதிகளைக் கழித்தோ கூட்டியோ கூட்டு உருவக் கணக்குகளைத் (ஒரு வயலைச் சுற்றிய பாதை, ஒரு கிணற்றைச் சுற்றிய கரை) தீர்த்தல்.',
    'உருக்கி மறுவார்ப்புக் கணக்குகள் – இங்கு மூலத் திண்மத்தின் கன அளவு புதிய திண்மத்தின்(களின்) கன அளவுக்குச் சமம்.',
    'நடைமுறைப் பயன்பாடுகள்: வேலி அமைக்கும் செலவு (சுற்றளவு அடிப்படையில்), வெள்ளையடிக்கும் அல்லது வண்ணம் பூசும் செலவு (புறப்பரப்பு அடிப்படையில்), கூம்பு வடிவக் கூடாரத்திற்குத் தேவையான துணி (வளைபரப்பு).'
  ],
  commonMistakesTitle: '3.3 பொதுவான தவறுகள்',
  commonMistakes: [
    'பரப்பளவு அல்லது கன அளவுச் சூத்திரங்களில் ஆரத்திற்குப் பதிலாக விட்டத்தைப் பயன்படுத்துதல்.',
    'உருளை, கூம்பு, அரைக்கோளம் ஆகியவற்றுக்கு வளைபரப்பையும் (CSA) மொத்தப் புறப்பரப்பையும் (TSA) குழப்பிக்கொள்ளுதல்.',
    'பரப்பளவு நீள அளவுமாற்றக் காரணியின் வர்க்கமாகவும், கன அளவு அதன் கனமாகவும் மாறுகின்றன – நீளத்தின் அதே காரணியால் அல்ல – என்பதை மறத்தல்.',
    'கூட்டு உருவக் கணக்குகளில், உள் பகுதியைக் கழிப்பதற்குப் பதிலாகக் கூட்டுதல், அல்லது நேர்மாறாகச் செய்தல்.',
    'உருக்கி மறுவார்ப்புக் கணக்குகளில், கன அளவுகளுக்குப் பதிலாகப் புறப்பரப்புகளைச் சமப்படுத்துதல்.',
    'அளவுகளைக் கூட்டும் அல்லது ஒப்பிடும் முன் அலகுகளை மாற்ற (எ.கா., செ.மீ-ஐ மீ ஆக) மறத்தல்.'
  ],
  examTipsTitle: '3.4 தேர்வுக் குறிப்புகள்',
  examTips: [
    'நேர அழுத்தத்தில் இவை அடிக்கடி குழப்பப்படுவதால், கணக்கிடும் முன் கேட்கப்படுவது எது – பரப்பளவு, கன அளவு, வளைபரப்பு, அல்லது மொத்தப் புறப்பரப்பு – என்பதைத் துல்லியமாக மீண்டும் கூறிக்கொள்ளவும்.',
    'அளவுமாற்றக் காரணிக் கணக்குகளில், ஒவ்வோர் உருவத்தின் அளவுகளையும் மீண்டும் கணக்கிடாமல், பரப்பளவு விகிதத்திற்கு k² மற்றும் கன அளவு விகிதத்திற்கு k³ ஐ நேரடியாகப் பயன்படுத்தவும்.',
    'கூட்டு உருவ (பாதை/கரை) கணக்குகளில், கழிக்கும் முன் வெளிப் பகுதியையும் உள் பகுதியையும் எப்போதும் தனித்தனியாகக் கணக்கிடவும்.',
    'உருக்கி மறுவார்ப்புக் கணக்குகளில், மூல மற்றும் புதிய திண்மங்களின் கன அளவுகளைச் சமப்படுத்தி, தெரியாத அளவைக் காணவும்.',
    'துல்லியமான விடைகளுக்கு, ஆரம் 7-இன் மடங்காக இருக்கும்போது (அல்லது பகுதி 7 ஆக வரும்போது) π = 22/7 ஐப் பயன்படுத்தவும்; இல்லையெனில் π ≈ 3.14 ஐப் பயன்படுத்தவும்.'
  ]
};
