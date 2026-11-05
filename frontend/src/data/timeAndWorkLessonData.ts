/** Exact Time and Work Lesson Theory extracted directly from TimeandWorkenglish and TimeandWorktamil PDFs. */
import type { LessonPdfData } from './ratioLessonData';

export const TIME_AND_WORK_PDF_EN: LessonPdfData = {
  lessonTitle: '3. Time and Work',
  objectivesTitle: '1. Learning Objectives',
  objectivesPreamble: 'The learner will be able to:',
  objectives: [
    'Express individual and combined work efficiencies using the unit-work (LCM) method.',
    'Apply the inverse relationship between number of workers/machines and time taken.',
    'Solve multi-person, alternate-day, pipes-and-cisterns, and wage-sharing problems involving combined work.',
    'Solve multi-step, competitive-examination-standard questions on Time and Work efficiently, using Strategic Planning, Time Management, Task Strategies, and Self-Monitoring.'
  ],
  overviewTitle: '2. Lesson Overview',
  overview:
    'Time and Work is a core Analytical Skills topic in TNPSC and allied competitive examinations, testing a candidate’s ability to interpret given information, analyse work efficiency, establish relationships between variables, and apply logical reasoning across multi-step problems. This revised lesson emphasises higher-order, multi-step problem solving – combined work with workers leaving or joining midway, alternate-day work, pipes and cisterns, and efficiency-based wage sharing – rather than simple one-step formula recall.',
  conceptTitle: '3. Concept Explanation',
  examInsightTitle: '3.1 Exam Insight',
  examInsight:
    'In TNPSC Group 1 and similar competitive examinations, Time and Work questions rarely stop at “A can do a job in n days.” They typically combine two or more conditions – a worker leaving or joining partway, an inlet and outlet pipe together, or a wage split by efficiency – and require the candidate to set up a relationship before solving. This lesson’s questions are built to that standard: each one requires at least two reasoning steps, not a single plug-in.',
  coreConceptsTitle: '3.2 Core Concepts',
  coreConceptsIntro:
    'Time and Work compares how much of a job is completed per unit time. In competitive examinations, learners should be proficient in:',
  coreConcepts: [
    'Expressing a person’s one-day work as 1/(days taken), and combining several people’s work by adding their rates.',
    'Using the LCM (unit-work) method to avoid fraction-heavy arithmetic when three or more workers are involved.',
    'Applying the inverse relationship between number of workers/machines and time taken.',
    'Handling problems where a worker leaves or joins partway, by tracking work completed as a running fraction of the total.',
    'Solving alternate-day work problems by computing work done per cycle, then handling any remaining partial day.',
    'Applying pipes-and-cisterns logic, where an outlet pipe’s rate is subtracted from the combined fill rate.',
    'Splitting wages or payment in the ratio of work contributed (equivalent to the efficiency ratio when time worked is equal).'
  ],
  commonMistakesTitle: '3.3 Common Mistakes',
  commonMistakes: [
    'Averaging individual times directly instead of adding efficiencies (rates).',
    'Forgetting to convert an efficiency percentage or ratio into a time ratio before applying the standard formula.',
    'In pipes-and-cisterns problems, treating an outlet pipe’s rate as an additional inlet instead of subtracting it.',
    'Using elapsed days instead of the actual fraction of work completed when workers change mid-task.',
    'In wage-sharing problems, dividing wages equally instead of in the ratio of efficiency/work contributed.'
  ],
  examTipsTitle: '3.4 Examination Tips',
  examTips: [
    'Default to the LCM (unit-work) method for combined-work problems involving three or more people – it removes fraction-heavy arithmetic.',
    'For “x% more efficient” statements, convert to an efficiency ratio first, then invert it to get the time ratio.',
    'Before calculating, restate in one line exactly what is being asked – total time, work left, wage share, or extra workers needed.',
    'For alternate-day and “leaves midway” problems, track work completed as a running fraction, not as days.',
    'In wage-sharing questions, always use the efficiency ratio (1/time), not the time ratio itself.'
  ]
};

export const TIME_AND_WORK_PDF_TA: LessonPdfData = {
  lessonTitle: '3. காலம் மற்றும் வேலை',
  objectivesTitle: '1. கற்றல் நோக்கங்கள்',
  objectivesPreamble: 'இப்பாடத்தை நிறைவு செய்த பின் கற்போர் பின்வருவனவற்றைச் செய்ய இயலும்:',
  objectives: [
    'அலகு-வேலை (மீ.பொ.ம) முறையைப் பயன்படுத்தித் தனி மற்றும் ஒருங்கிணைந்த வேலைத் திறன்களை வெளிப்படுத்துதல்.',
    'பணியாளர்கள்/இயந்திரங்களின் எண்ணிக்கைக்கும் எடுக்கும் காலத்திற்கும் இடையிலான எதிர்த் தொடர்பைப் பயன்படுத்துதல்.',
    'பலர் சேர்ந்து செய்யும் வேலை, மாற்று நாள் வேலை, குழாய்களும் தொட்டிகளும், கூலிப் பகிர்வு ஆகிய ஒருங்கிணைந்த வேலைக் கணக்குகளைத் தீர்த்தல்.',
    'உத்தித் திட்டமிடல், நேர மேலாண்மை, பணி உத்திகள், சுயக் கண்காணிப்பு ஆகியவற்றைப் பயன்படுத்தி, போட்டித் தேர்வுத் தரத்திலான பல படிநிலைக் காலம் மற்றும் வேலை வினாக்களைத் திறம்படத் தீர்த்தல்.'
  ],
  overviewTitle: '2. பாடக் கண்ணோட்டம்',
  overview:
    'காலம் மற்றும் வேலை என்பது TNPSC மற்றும் அது சார்ந்த போட்டித் தேர்வுகளில் ஒரு முக்கியப் பகுப்பாய்வுத் திறன் தலைப்பாகும். கொடுக்கப்பட்ட தகவலைப் புரிந்துகொள்ளுதல், வேலைத் திறனைப் பகுப்பாய்தல், மாறிகளுக்கிடையிலான தொடர்புகளை அமைத்தல், பல படிநிலைக் கணக்குகளில் தர்க்க ரீதியாகச் சிந்தித்தல் ஆகிய தேர்வரின் திறன்களை இது சோதிக்கிறது. இத்திருத்திய பாடம் எளிய ஒருபடி சூத்திர நினைவுகூர்தலுக்குப் பதிலாக, உயர்நிலை, பல படிநிலைச் சிக்கல் தீர்த்தலுக்கு – இடையில் பணியாளர்கள் விலகும் அல்லது சேரும் ஒருங்கிணைந்த வேலை, மாற்று நாள் வேலை, குழாய்களும் தொட்டிகளும், திறன் அடிப்படையிலான கூலிப் பகிர்வு – முக்கியத்துவம் அளிக்கிறது.',
  conceptTitle: '3. கருத்து விளக்கம்',
  examInsightTitle: '3.1 தேர்வு நோக்கு',
  examInsight:
    'TNPSC குரூப் 1 மற்றும் இதுபோன்ற போட்டித் தேர்வுகளில், காலம் மற்றும் வேலை வினாக்கள் “A ஒரு வேலையை n நாட்களில் செய்ய முடியும்” என்பதோடு நிற்பது அரிது. அவை பொதுவாக இரண்டு அல்லது அதற்கு மேற்பட்ட நிபந்தனைகளை – இடையில் விலகும் அல்லது சேரும் பணியாளர், ஒரே நேரத்தில் நிரப்பும் மற்றும் வெளியேற்றும் குழாய்கள், அல்லது திறன் அடிப்படையிலான கூலிப் பகிர்வு – இணைக்கின்றன; தீர்ப்பதற்கு முன் தேர்வர் ஒரு தொடர்பை அமைக்க வேண்டியுள்ளது. இப்பாடத்தின் வினாக்கள் அந்த தரத்தில் அமைக்கப்பட்டுள்ளன: ஒவ்வொரு வினாவும் ஒரே ஒரு மதிப்பைப் பிரதியிடுவதாக இல்லாமல், குறைந்தது இரண்டு தர்க்கப் படிநிலைகளைக் கோருகிறது.',
  coreConceptsTitle: '3.2 அடிப்படைக் கருத்துகள்',
  coreConceptsIntro:
    'காலம் மற்றும் வேலை என்பது ஓர் அலகு நேரத்தில் ஒரு வேலையின் எவ்வளவு பகுதி முடிக்கப்படுகிறது என்பதை ஒப்பிடுகிறது. போட்டித் தேர்வுகளில் கற்போர் பின்வருவனவற்றில் தேர்ச்சி பெற்றிருக்க வேண்டும்:',
  coreConcepts: [
    'ஒருவரின் ஒரு நாள் வேலையை 1/(எடுத்துக்கொண்ட நாட்கள்) என வெளிப்படுத்துதல்; பலரின் வேலையை அவர்களின் வீதங்களைக் கூட்டி இணைத்தல்.',
    'மூன்று அல்லது அதற்கு மேற்பட்ட பணியாளர்கள் இருக்கும்போது, பின்னக் கணக்கீடுகளைத் தவிர்க்க மீ.பொ.ம (அலகு-வேலை) முறையைப் பயன்படுத்துதல்.',
    'பணியாளர்கள்/இயந்திரங்களின் எண்ணிக்கைக்கும் எடுக்கும் காலத்திற்கும் இடையிலான எதிர்த் தொடர்பைப் பயன்படுத்துதல்.',
    'இடையில் ஒரு பணியாளர் விலகும் அல்லது சேரும் கணக்குகளில், முடிக்கப்பட்ட வேலையை மொத்தத்தின் தொடர் பின்னமாகக் கண்காணித்துத் தீர்த்தல்.',
    'மாற்று நாள் வேலைக் கணக்குகளில், ஒரு சுழற்சியில் முடிக்கப்படும் வேலையைக் கணக்கிட்டு, பின்னர் மீதமுள்ள பகுதி நாளைக் கையாளுதல்.',
    'குழாய்களும் தொட்டிகளும் தர்க்கத்தைப் பயன்படுத்துதல் – இதில் வெளியேற்றும் குழாயின் வீதம் ஒருங்கிணைந்த நிரப்பும் வீதத்திலிருந்து கழிக்கப்படுகிறது.',
    'செய்த வேலையின் விகிதத்தில் கூலி அல்லது தொகையைப் பகிர்தல் (வேலை செய்த காலம் சமமாக இருக்கும்போது இது திறன் விகிதத்திற்குச் சமம்).'
  ],
  commonMistakesTitle: '3.3 பொதுவான தவறுகள்',
  commonMistakes: [
    'திறன்களை (வீதங்களை) கூட்டுவதற்குப் பதிலாகத் தனிக் காலங்களின் சராசரியை நேரடியாக எடுத்தல்.',
    'வழக்கமான சூத்திரத்தைப் பயன்படுத்தும் முன், திறன் சதவீதம் அல்லது விகிதத்தைக் கால விகிதமாக மாற்ற மறத்தல்.',
    'குழாய்களும் தொட்டிகளும் கணக்குகளில், வெளியேற்றும் குழாயின் வீதத்தைக் கழிப்பதற்குப் பதிலாகக் கூடுதல் நிரப்பும் குழாயாகக் கருதுதல்.',
    'வேலையின் இடையில் பணியாளர்கள் மாறும்போது, உண்மையில் முடிக்கப்பட்ட வேலைப் பின்னத்திற்குப் பதிலாகக் கடந்த நாட்களைப் பயன்படுத்துதல்.',
    'கூலிப் பகிர்வுக் கணக்குகளில், திறன்/செய்த வேலையின் விகிதத்தில் பகிர்வதற்குப் பதிலாகக் கூலியைச் சமமாகப் பிரித்தல்.'
  ],
  examTipsTitle: '3.4 தேர்வுக் குறிப்புகள்',
  examTips: [
    'மூன்று அல்லது அதற்கு மேற்பட்டோர் சேர்ந்து செய்யும் வேலைக் கணக்குகளுக்கு இயல்பாகவே மீ.பொ.ம (அலகு-வேலை) முறையைப் பயன்படுத்தவும் – இது பின்னக் கணக்கீடுகளைத் தவிர்க்கிறது.',
    '“x% அதிகத் திறன்” என்ற கூற்றுகளுக்கு, முதலில் திறன் விகிதமாக மாற்றி, பின்னர் அதைத் தலைகீழாக்கிக் கால விகிதத்தைப் பெறவும்.',
    'கணக்கிடும் முன், எது கேட்கப்படுகிறது என்பதை – மொத்தக் காலம், மீதமுள்ள வேலை, கூலிப் பங்கு, அல்லது தேவைப்படும் கூடுதல் பணியாளர்கள் – ஒரே வரியில் மீண்டும் கூறிக்கொள்ளவும்.',
    'மாற்று நாள் மற்றும் “இடையில் விலகும்” கணக்குகளில், முடிக்கப்பட்ட வேலையை நாட்களாக அல்லாமல் தொடர் பின்னமாகக் கண்காணிக்கவும்.',
    'கூலிப் பகிர்வு வினாக்களில், கால விகிதத்தை அல்லாமல் எப்போதும் திறன் விகிதத்தை (1/காலம்) பயன்படுத்தவும்.'
  ]
};
