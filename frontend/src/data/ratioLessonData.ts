/** Exact Ratio and Proportion Lesson Theory extracted directly from RatioandProportionenglish and RatioandProportiontamil PDFs. */

export interface LessonPdfData {
  lessonTitle: string;
  objectivesTitle: string;
  objectivesPreamble: string;
  objectives: string[];
  overviewTitle: string;
  overview: string;
  conceptTitle: string;
  examInsightTitle: string;
  examInsight: string;
  coreConceptsTitle: string;
  coreConceptsIntro: string;
  coreConcepts: string[];
  commonMistakesTitle: string;
  commonMistakes: string[];
  examTipsTitle: string;
  examTips: string[];
}

export const RATIO_PDF_EN: LessonPdfData = {
  lessonTitle: '2. Ratio and Proportion',
  objectivesTitle: '1. Learning Objectives',
  objectivesPreamble: 'The learner will be able to:',
  objectives: [
    'Simplify and compare ratios accurately.',
    'Divide quantities and solve proportion-based problems.',
    'Apply ratio and proportion concepts to real-life and examination contexts.',
    'Solve multi-step, competitive-examination-standard questions on ratio and proportion efficiently.'
  ],
  overviewTitle: '2. Lesson Overview',
  overview:
    'Ratio and Proportion is one of the most frequently tested topics in competitive examinations such as TNPSC Group 1. It forms the foundation for solving questions related to partnership, mixture and alligation, time and work, ages, and profit and loss. This lesson emphasises higher-order, multi-step problem solving -- translating real-life and examination-style scenarios into ratio equations -- rather than simple formula recall.',
  conceptTitle: '3. Concept Explanation',
  examInsightTitle: '3.1 Exam Insight',
  examInsight:
    "In TNPSC and similar competitive examinations, Ratio and Proportion questions rarely test a bare formula in isolation. They are usually embedded in a real-world context -- partnership profits, mixtures, ages, speeds, or population change -- and require the candidate to set up an equation from the given condition before solving. This lesson's questions are built to that standard: each one requires at least two reasoning steps, not a single plug-in.",
  coreConceptsTitle: '3.2 Core Concepts',
  coreConceptsIntro:
    'Ratio and Proportion compares and relates quantities. In competitive examinations, learners should be proficient in:',
  coreConcepts: [
    'Expressing the relationship between two or more quantities of the same kind as a ratio.',
    'Simplifying ratios and comparing two or more ratios.',
    'Dividing a given quantity into parts according to a specified ratio, including when a difference (not a sum) is given.',
    'Finding the fourth, third, and mean proportional, and working with continued proportion.',
    'Distinguishing between direct proportion, inverse proportion, and joint (combined) variation.',
    'Working with compounded, duplicate, and sub-duplicate ratios, including their use in map-scale and area problems.',
    'Applying ratio and proportion to partnership (including time-weighted capital), mixtures, ages projected forward or backward in time, and comparative (set-overlap) scenarios.'
  ],
  commonMistakesTitle: '3.3 Common Mistakes',
  commonMistakes: [
    'Comparing ratios without expressing them with a common base or common terms.',
    'Adding or subtracting ratios directly instead of converting to a common multiple.',
    'Confusing direct proportion with inverse proportion in word problems.',
    'Losing the unit (parts vs. actual quantity) while dividing a quantity in a given ratio.',
    'In partnership problems, using capital alone and ignoring the time period each partner\'s capital was invested for.',
    'In area/map-scale problems, applying the linear scale directly instead of squaring it.'
  ],
  examTipsTitle: '3.4 Examination Tips',
  examTips: [
    'Express all ratios in their simplest form before comparing or combining them.',
    'To combine two ratios (A:B and B:C) into A:B:C, make the common term equal in both ratios.',
    'Assume a variable multiplier (x or k) to convert ratio parts into actual quantities, especially when a condition (sum, difference, product, or a value after change) is given.',
    'Check whether the quantities vary directly, inversely, or jointly before setting up the proportion.',
    'For partnership problems, always multiply capital by time invested before forming the profit-sharing ratio.',
    'Re-read multi-step questions carefully to identify exactly which quantity is being asked for, since intermediate values are often close to the answer options.'
  ]
};

export const RATIO_PDF_TA: LessonPdfData = {
  lessonTitle: '2. விகிதம் மற்றும் விகிதசமம்',
  objectivesTitle: '1. கற்றல் நோக்கங்கள்',
  objectivesPreamble: 'இப்பாடத்தை நிறைவு செய்த பின் கற்போர் பின்வருவனவற்றைச் செய்ய இயலும்:',
  objectives: [
    'விகிதங்களைத் துல்லியமாகச் சுருக்குதல் மற்றும் ஒப்பிடுதல்.',
    'அளவுகளைப் பிரித்தல் மற்றும் விகிதசமம் சார்ந்த கணக்குகளைத் தீர்த்தல்.',
    'விகிதம் மற்றும் விகிதசமக் கருத்துகளை அன்றாட வாழ்க்கை மற்றும் தேர்வுச் சூழல்களில் பயன்படுத்துதல்.',
    'போட்டித் தேர்வுத் தரத்திலான, பல படிநிலை விகிதம் மற்றும் விகிதசம வினாக்களைத் திறம்படத் தீர்த்தல்.'
  ],
  overviewTitle: '2. பாடக் கண்ணோட்டம்',
  overview:
    'TNPSC குரூப் 1 போன்ற போட்டித் தேர்வுகளில் அடிக்கடி கேட்கப்படும் தலைப்புகளில் விகிதம் மற்றும் விகிதசமம் ஒன்றாகும். கூட்டாண்மை, கலவை மற்றும் கலப்பு விதி, காலம் மற்றும் வேலை, வயது, இலாபம் மற்றும் நட்டம் தொடர்பான வினாக்களைத் தீர்ப்பதற்கு இதுவே அடிப்படையாக அமைகிறது. இப்பாடம் எளிய சூத்திர நினைவுகூர்தலுக்குப் பதிலாக, உயர்நிலை, பல படிநிலைச் சிக்கல் தீர்த்தலுக்கு -- அன்றாட வாழ்க்கை மற்றும் தேர்வு வகைச் சூழல்களை விகிதச் சமன்பாடுகளாக மாற்றுவதற்கு -- முக்கியத்துவம் அளிக்கிறது.',
  conceptTitle: '3. கருத்து விளக்கம்',
  examInsightTitle: '3.1 தேர்வு நோக்கு',
  examInsight:
    "TNPSC மற்றும் இதுபோன்ற போட்டித் தேர்வுகளில், விகிதம் மற்றும் விகிதசம வினாக்கள் ஒரு சூத்திரத்தை மட்டும் தனித்துச் சோதிப்பது அரிது. அவை பொதுவாக ஒரு நடைமுறைச் சூழலில் -- கூட்டாண்மை இலாபம், கலவைகள், வயது, வேகம், அல்லது மக்கள்தொகை மாற்றம் -- அமைந்திருக்கும்; தீர்ப்பதற்கு முன் கொடுக்கப்பட்ட நிபந்தனையிலிருந்து தேர்வர் ஒரு சமன்பாட்டை அமைக்க வேண்டும். இப்பாடத்தின் வினாக்கள் அந்த தரத்தில் அமைக்கப்பட்டுள்ளன: ஒவ்வொரு வினாவும் ஒரே ஒரு மதிப்பைப் பிரதியிடுவதாக இல்லாமல், குறைந்தது இரண்டு தர்க்கப் படிநிலைகளைக் கோருகிறது.",
  coreConceptsTitle: '3.2 அடிப்படைக் கருத்துகள்',
  coreConceptsIntro:
    'விகிதம் மற்றும் விகிதசமம் அளவுகளை ஒப்பிட்டு, அவற்றுக்கிடையிலான தொடர்பை விளக்குகிறது. போட்டித் தேர்வுகளில் கற்போர் பின்வருவனவற்றில் தேர்ச்சி பெற்றிருக்க வேண்டும்:',
  coreConcepts: [
    'ஒரே வகையைச் சேர்ந்த இரண்டு அல்லது அதற்கு மேற்பட்ட அளவுகளுக்கிடையிலான தொடர்பை விகிதமாக வெளிப்படுத்துதல்.',
    'விகிதங்களைச் சுருக்குதல் மற்றும் இரண்டு அல்லது அதற்கு மேற்பட்ட விகிதங்களை ஒப்பிடுதல்.',
    'கொடுக்கப்பட்ட அளவைக் குறிப்பிட்ட விகிதத்தில் பகுதிகளாகப் பிரித்தல்; கூடுதலுக்குப் பதிலாக வேறுபாடு கொடுக்கப்படும் நிலையும் இதில் அடங்கும்.',
    'நான்காம், மூன்றாம் மற்றும் இடை விகிதசம உறுப்புகளைக் காணுதல், தொடர் விகிதசமத்துடன் செயல்படுதல்.',
    'நேர் விகிதசமம், எதிர் விகிதசமம் மற்றும் கூட்டு (இணை) மாறுபாடு ஆகியவற்றை வேறுபடுத்துதல்.',
    'கூட்டு விகிதம், இருமடி விகிதம், வர்க்கமூல விகிதம் ஆகியவற்றுடன் செயல்படுதல்; வரைபட அளவுகோல் மற்றும் பரப்புக் கணக்குகளில் அவற்றைப் பயன்படுத்துதல் உட்பட.',
    'கூட்டாண்மை (கால அடிப்படையிலான முதலீடு உட்பட), கலவைகள், முன்னோக்கி அல்லது பின்னோக்கிக் கணக்கிடப்படும் வயது, ஒப்பீட்டு (கண மேற்பொருந்துதல்) சூழல்கள் ஆகியவற்றில் விகிதம் மற்றும் விகிதசமத்தைப் பயன்படுத்துதல்.'
  ],
  commonMistakesTitle: '3.3 பொதுவான தவறுகள்',
  commonMistakes: [
    'பொது அடிப்படை அல்லது பொது உறுப்புகளாக மாற்றாமல் விகிதங்களை ஒப்பிடுதல்.',
    'பொது மடங்காக மாற்றுவதற்குப் பதிலாக விகிதங்களை நேரடியாகக் கூட்டுதல் அல்லது கழித்தல்.',
    'சொற்கணக்குகளில் நேர் விகிதசமத்தையும் எதிர் விகிதசமத்தையும் குழப்பிக்கொள்ளுதல்.',
    'ஓர் அளவைக் கொடுக்கப்பட்ட விகிதத்தில் பிரிக்கும்போது அலகை (பகுதிகள் / உண்மையான அளவு) தவறவிடுதல்.',
    'கூட்டாண்மைக் கணக்குகளில், ஒவ்வொரு கூட்டாளியின் முதலீடு எவ்வளவு காலம் இருந்தது என்பதைப் புறக்கணித்து, முதலீட்டை மட்டும் பயன்படுத்துதல்.',
    'பரப்பு/வரைபட அளவுகோல் கணக்குகளில், நேரியல் அளவுகோலை வர்க்கப்படுத்தாமல் நேரடியாகப் பயன்படுத்துதல்.'
  ],
  examTipsTitle: '3.4 தேர்வுக் குறிப்புகள்',
  examTips: [
    'விகிதங்களை ஒப்பிடும் அல்லது இணைக்கும் முன், அனைத்தையும் அவற்றின் எளிய வடிவில் எழுதவும்.',
    'A:B மற்றும் B:C என்ற இரண்டு விகிதங்களை A:B:C ஆக இணைக்க, இரண்டு விகிதங்களிலும் பொது உறுப்பைச் சமமாக்கவும்.',
    'விகிதப் பகுதிகளை உண்மையான அளவுகளாக மாற்ற, ஒரு மாறிப் பெருக்கியை (x அல்லது k) கொள்க; குறிப்பாகக் கூடுதல், வேறுபாடு, பெருக்கற்பலன் அல்லது மாற்றத்திற்குப் பிந்தைய மதிப்பு போன்ற நிபந்தனை கொடுக்கப்படும்போது.',
    'விகிதசமத்தை அமைக்கும் முன், அளவுகள் நேர், எதிர் அல்லது கூட்டு முறையில் மாறுகின்றனவா எனச் சரிபார்க்கவும்.',
    'கூட்டாண்மைக் கணக்குகளில், இலாபப் பகிர்வு விகிதத்தை அமைக்கும் முன் எப்போதும் முதலீட்டைக் காலத்தால் பெருக்கவும்.',
    'இடைநிலை மதிப்புகள் பெரும்பாலும் விடைத் தேர்வுகளுக்கு நெருக்கமாக இருப்பதால், எந்த அளவு கேட்கப்படுகிறது என்பதைத் துல்லியமாக அறிய பல படிநிலை வினாக்களைக் கவனமாக மீண்டும் படிக்கவும்.'
  ]
};
