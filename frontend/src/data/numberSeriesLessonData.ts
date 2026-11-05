/** Exact Number Series Lesson Theory extracted directly from NumberSeriesenglish and NumberSeriestamil PDFs. */
import type { LessonPdfData } from './ratioLessonData';

export const NUMBER_SERIES_PDF_EN: LessonPdfData = {
  lessonTitle: '6. Number Series',
  objectivesTitle: '1. Learning Objectives',
  objectivesPreamble: 'The learner will be able to:',
  objectives: [
    'Identify numerical patterns including arithmetic, geometric, square, cube, and prime-number series.',
    'Solve alternating-operation and two-interleaved series problems.',
    'Identify the wrong number in a series and find missing terms, including terms in the middle of a sequence.',
    'Solve multi-step, competitive-examination-standard questions on Number Series efficiently, using Attention Control, Task Strategies, Self-Monitoring, and Self-Evaluation & Reflection.'
  ],
  overviewTitle: '2. Lesson Overview',
  overview:
    'Number Series is a core Logical Reasoning Skills topic in TNPSC Group 1 and allied competitive examinations, testing a candidate’s ability to identify numerical patterns, recognise underlying relationships, and predict subsequent terms through logical analysis. This lesson emphasises higher-order, multi-step problem solving – alternating operations, two-interleaved series, wrong-number identification, and missing middle terms – rather than simple constant-difference recall.',
  conceptTitle: '3. Concept Explanation',
  examInsightTitle: '3.1 Exam Insight',
  examInsight:
    'In TNPSC Group 1 and similar competitive examinations, Number Series questions rarely stop at “find the next term in a simple arithmetic series.” They typically involve a changing gap, an alternating pair of operations, two series interleaved into one, a deliberately wrong term to identify, or a missing term in the middle of the sequence – and require the candidate to test more than one pattern type before settling on the correct one. This lesson’s questions are built to that standard.',
  coreConceptsTitle: '3.2 Core Concepts',
  coreConceptsIntro:
    'A number series is a sequence of numbers following a definite pattern. In competitive examinations, learners should be proficient in recognising:',
  coreConcepts: [
    'Arithmetic series: a constant difference between consecutive terms (e.g., +2, +2, +2…).',
    'Geometric series: a constant ratio between consecutive terms (e.g., ×2, ×2, ×2…).',
    'Series with an increasing or decreasing gap (e.g., +2, +3, +4, +5…).',
    'Square and cube series (e.g., 1, 4, 9, 16… or 1, 8, 27, 64…).',
    'Prime number series and Fibonacci-type series (each term is the sum of the two preceding terms).',
    'Mixed-operation series (e.g., ×2 then −1, repeating).',
    'Two-interleaved series, where alternating positions (1st, 3rd, 5th… and 2nd, 4th, 6th…) each follow their own independent pattern.',
    'Wrong-number identification, where one term breaks an otherwise consistent pattern.',
    'Missing middle-term problems, where a term partway through the series must be found using the surrounding terms.'
  ],
  commonMistakesTitle: '3.3 Common Mistakes',
  commonMistakes: [
    'Assuming a series is arithmetic (constant difference) without checking whether the gap itself is changing.',
    'In alternating-operation series, applying the same single operation throughout instead of identifying the repeating pair of operations.',
    'In two-interleaved series, trying to find one pattern across all terms instead of splitting the series into odd-position and even-position sub-series.',
    'In wrong-number problems, changing the answer to fit the wrong term instead of identifying which term breaks the pattern.',
    'In missing middle-term problems, only checking the pattern from one side instead of verifying it against terms on both sides.',
    'Stopping at the first pattern that fits two or three terms without verifying it against the entire series.'
  ],
  examTipsTitle: '3.4 Examination Tips',
  examTips: [
    'First check the simplest pattern (constant difference or constant ratio) before testing more complex patterns like squares, cubes, or alternating operations.',
    'For a series with a changing gap, write out the differences between consecutive terms as a separate row – this often reveals a simpler underlying pattern.',
    'For two-interleaved series, list the odd-position and even-position terms separately before searching for a pattern.',
    'For wrong-number questions, compute the expected pattern for all terms first, then compare against the given series to spot the mismatch.',
    'Always verify a suspected pattern against every term in the series, not just the first two or three, before finalising the answer.'
  ]
};

export const NUMBER_SERIES_PDF_TA: LessonPdfData = {
  lessonTitle: '6. எண் தொடர்கள் (Number Series)',
  objectivesTitle: '1. கற்றல் நோக்கங்கள்',
  objectivesPreamble: 'இப்பாடத்தை நிறைவு செய்த பின் கற்போர் பின்வருவனவற்றைச் செய்ய இயலும்:',
  objectives: [
    'கூட்டுத் தொடர், பெருக்குத் தொடர், வர்க்கம், கனம், பகா எண் தொடர்கள் உள்ளிட்ட எண் அமைப்புகளை அடையாளம் காணுதல்.',
    'மாறி மாறி வரும் செயல்கள் மற்றும் இரு இடையிட்ட தொடர்கள் சார்ந்த கணக்குகளைத் தீர்த்தல்.',
    'ஒரு தொடரில் உள்ள தவறான எண்ணை அடையாளம் காணுதல் மற்றும் தொடரின் நடுவில் உள்ளவை உட்பட விடுபட்ட உறுப்புகளைக் காணுதல்.',
    'கவனக் கட்டுப்பாடு, பணி உத்திகள், சுயக் கண்காணிப்பு, சுய மதிப்பீடு மற்றும் சிந்தனை ஆகியவற்றைப் பயன்படுத்தி, போட்டித் தேர்வுத் தரத்திலான பல படிநிலை எண் தொடர் வினாக்களைத் திறம்படத் தீர்த்தல்.'
  ],
  overviewTitle: '2. பாடக் கண்ணோட்டம்',
  overview:
    'எண் தொடர்கள் என்பது TNPSC குரூப் 1 மற்றும் அது சார்ந்த போட்டித் தேர்வுகளில் ஒரு முக்கியத் தருக்கத் திறன் தலைப்பாகும். எண் அமைப்புகளை அடையாளம் காணுதல், அடிப்படைத் தொடர்புகளை அறிதல், தருக்கப் பகுப்பாய்வின் மூலம் அடுத்த உறுப்புகளை முன்கணித்தல் ஆகிய தேர்வரின் திறன்களை இது சோதிக்கிறது. இப்பாடம் எளிய மாறா வித்தியாச நினைவுகூர்தலுக்குப் பதிலாக, உயர்நிலை, பல படிநிலைச் சிக்கல் தீர்த்தலுக்கு – மாறி மாறி வரும் செயல்கள், இரு இடையிட்ட தொடர்கள், தவறான எண்ணை அடையாளம் காணுதல், நடுவில் விடுபட்ட உறுப்புகள் – முக்கியத்துவம் அளிக்கிறது.',
  conceptTitle: '3. கருத்து விளக்கம்',
  examInsightTitle: '3.1 தேர்வு நோக்கு',
  examInsight:
    'TNPSC குரூப் 1 மற்றும் இதுபோன்ற போட்டித் தேர்வுகளில், எண் தொடர் வினாக்கள் “எளிய கூட்டுத் தொடரில் அடுத்த உறுப்பைக் காண்க” என்பதோடு நிற்பது அரிது. அவை பொதுவாக மாறும் இடைவெளி, மாறி மாறி வரும் இரு செயல்கள், ஒன்றாக இடையிட்ட இரு தொடர்கள், அடையாளம் காண வேண்டிய வேண்டுமென்றே தவறான உறுப்பு, அல்லது தொடரின் நடுவில் விடுபட்ட உறுப்பு ஆகியவற்றைக் கொண்டிருக்கும்; சரியான அமைப்பை முடிவு செய்யும் முன் தேர்வர் ஒன்றுக்கு மேற்பட்ட அமைப்பு வகைகளைச் சோதிக்க வேண்டியுள்ளது. இப்பாடத்தின் வினாக்கள் அந்த தரத்தில் அமைக்கப்பட்டுள்ளன.',
  coreConceptsTitle: '3.2 அடிப்படைக் கருத்துகள்',
  coreConceptsIntro:
    'எண் தொடர் என்பது ஒரு திட்டவட்டமான அமைப்பைப் பின்பற்றும் எண்களின் வரிசையாகும். போட்டித் தேர்வுகளில் கற்போர் பின்வருவனவற்றை அடையாளம் காண்பதில் தேர்ச்சி பெற்றிருக்க வேண்டும்:',
  coreConcepts: [
    'கூட்டுத் தொடர்: அடுத்தடுத்த உறுப்புகளுக்கிடையே மாறா வித்தியாசம் (எ.கா., +2, +2, +2…).',
    'பெருக்குத் தொடர்: அடுத்தடுத்த உறுப்புகளுக்கிடையே மாறா விகிதம் (எ.கா., ×2, ×2, ×2…).',
    'அதிகரிக்கும் அல்லது குறையும் இடைவெளி கொண்ட தொடர்கள் (எ.கா., +2, +3, +4, +5…).',
    'வர்க்க மற்றும் கனத் தொடர்கள் (எ.கா., 1, 4, 9, 16… அல்லது 1, 8, 27, 64…).',
    'பகா எண் தொடர் மற்றும் ஃபிபோனச்சி வகைத் தொடர் (ஒவ்வோர் உறுப்பும் முந்தைய இரண்டு உறுப்புகளின் கூடுதல்).',
    'கலப்புச் செயல் தொடர் (எ.கா., ×2 பின்னர் −1, மீண்டும் மீண்டும்).',
    'இரு இடையிட்ட தொடர் – இதில் மாற்று இடங்கள் (1, 3, 5… மற்றும் 2, 4, 6…) ஒவ்வொன்றும் தனக்கென ஒரு தனி அமைப்பைப் பின்பற்றுகின்றன.',
    'தவறான எண்ணை அடையாளம் காணுதல் – இதில் ஓர் உறுப்பு, இல்லையெனில் சீரான அமைப்பை உடைக்கிறது.',
    'நடுவில் விடுபட்ட உறுப்புக் கணக்குகள் – இதில் தொடரின் இடையிலுள்ள ஓர் உறுப்பைச் சுற்றியுள்ள உறுப்புகளைக் கொண்டு காண வேண்டும்.'
  ],
  commonMistakesTitle: '3.3 பொதுவான தவறுகள்',
  commonMistakes: [
    'இடைவெளியே மாறுகிறதா எனச் சரிபார்க்காமல், ஒரு தொடரைக் கூட்டுத் தொடர் (மாறா வித்தியாசம்) எனக் கருதுதல்.',
    'மாறி மாறி வரும் செயல் தொடர்களில், மீண்டும் வரும் செயல் இணையைக் கண்டறியாமல், ஒரே செயலை முழுவதும் பயன்படுத்துதல்.',
    'இரு இடையிட்ட தொடர்களில், தொடரை ஒற்றை இட மற்றும் இரட்டை இட உட்தொடர்களாகப் பிரிக்காமல், அனைத்து உறுப்புகளுக்கும் ஒரே அமைப்பைக் காண முயலுதல்.',
    'தவறான எண் கணக்குகளில், அமைப்பை உடைக்கும் உறுப்பை அடையாளம் காணாமல், தவறான உறுப்புக்குப் பொருந்துமாறு விடையை மாற்றுதல்.',
    'நடுவில் விடுபட்ட உறுப்புக் கணக்குகளில், இருபுறமும் உள்ள உறுப்புகளுடன் சரிபார்க்காமல், ஒருபுறத்திலிருந்து மட்டும் அமைப்பைச் சரிபார்த்தல்.',
    'முழுத் தொடருடன் சரிபார்க்காமல், இரண்டு அல்லது மூன்று உறுப்புகளுக்குப் பொருந்தும் முதல் அமைப்பிலேயே நின்றுவிடுதல்.'
  ],
  examTipsTitle: '3.4 தேர்வுக் குறிப்புகள்',
  examTips: [
    'வர்க்கங்கள், கனங்கள், மாறி மாறி வரும் செயல்கள் போன்ற சிக்கலான அமைப்புகளைச் சோதிக்கும் முன், எளிய அமைப்பை (மாறா வித்தியாசம் அல்லது மாறா விகிதம்) முதலில் சரிபார்க்கவும்.',
    'மாறும் இடைவெளி கொண்ட தொடருக்கு, அடுத்தடுத்த உறுப்புகளின் வித்தியாசங்களைத் தனி வரிசையாக எழுதவும் – இது பெரும்பாலும் எளிய அடிப்படை அமைப்பை வெளிப்படுத்தும்.',
    'இரு இடையிட்ட தொடர்களுக்கு, அமைப்பைத் தேடும் முன் ஒற்றை இட மற்றும் இரட்டை இட உறுப்புகளைத் தனித்தனியாகப் பட்டியலிடவும்.',
    'தவறான எண் வினாக்களுக்கு, முதலில் அனைத்து உறுப்புகளுக்குமான எதிர்பார்க்கப்படும் அமைப்பைக் கணக்கிட்டு, பின்னர் கொடுக்கப்பட்ட தொடருடன் ஒப்பிட்டுப் பொருந்தாததைக் கண்டறியவும்.',
    'விடையை இறுதி செய்யும் முன், ஊகித்த அமைப்பை முதல் இரண்டு அல்லது மூன்று உறுப்புகளுடன் மட்டுமல்லாமல், தொடரின் ஒவ்வோர் உறுப்புடனும் எப்போதும் சரிபார்க்கவும்.'
  ]
};
