/** Exact Percentage Lesson Theory extracted directly from PercentageEnglish and PercentageTamil PDFs. */

export interface PercentagePdfLesson {
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

export const PERCENTAGE_PDF_EN: PercentagePdfLesson = {
  lessonTitle: '1. Percentage',
  objectivesTitle: '1. Learning Objectives',
  objectivesPreamble: 'The learner will be able to:',
  objectives: [
    'Calculate percentages, percentage increase, and percentage decrease accurately.',
    'Solve reverse-percentage and successive-percentage-change problems.',
    'Apply percentage concepts to real-life and examination contexts (profit-loss, population, discounts, mixtures).',
    'Solve multi-step, competitive-examination-standard questions on percentage efficiently.'
  ],
  overviewTitle: '2. Lesson Overview',
  overview:
    'Percentage is one of the most fundamental and frequently tested topics in competitive examinations such as TNPSC Group 1. It underlies profit and loss, discount, population growth, data interpretation, and simple interest questions. This revised lesson emphasizes higher-order, multi-step problem solving -- successive percentage changes, reverse percentage, comparative and overlap (Venn-style) problems -- rather than simple one-step formula recall.',
  conceptTitle: '3. Concept Explanation',
  examInsightTitle: '3.1 Exam Insight',
  examInsight:
    "In TNPSC Group 1 and similar competitive examinations, percentage questions are rarely a bare 'find X% of Y' calculation. They typically combine two or more conditions -- successive changes, a margin or difference, two related quantities, or an overlap between categories -- and require the candidate to set up a relationship before solving. This lesson's questions are built to that standard: each one requires at least two reasoning steps, not a single plug-in.",
  coreConceptsTitle: '3.2 Core Concepts',
  coreConceptsIntro:
    'Percentage compares a part to a whole, expressed out of 100. In competitive examinations, learners should be proficient in:',
  coreConcepts: [
    'Converting between fractions, decimals, and percentages, and finding a percentage of a given quantity.',
    'Calculating percentage increase and percentage decrease, including reverse percentage (finding the original value).',
    'Applying successive percentage changes (two or more changes applied one after another) correctly via multiplying factors.',
    'Distinguishing a change in percentage points from a percentage (relative) change in the underlying quantity.',
    'Solving comparative percentage problems (e.g., two candidates, two related quantities such as income and expenditure).',
    'Applying percentage to profit and loss, successive discounts, mixtures/concentrations, and population or depreciation over multiple periods.',
    'Solving overlap (Venn-style) percentage problems involving two categories and their intersection.'
  ],
  commonMistakesTitle: '3.3 Common Mistakes',
  commonMistakes: [
    'Adding or subtracting successive percentage changes directly instead of multiplying the corresponding factors.',
    'Confusing a change in percentage points with a percentage (relative) increase or decrease.',
    'Applying a discount or profit percentage to the wrong base (marked price vs. cost price vs. selling price).',
    'In reverse-percentage problems, dividing by the percentage value itself instead of by the correct multiplying factor.',
    'In overlap (Venn-style) problems, forgetting to account for the intersection when combining two percentages.'
  ],
  examTipsTitle: '3.4 Examination Tips',
  examTips: [
    'For successive percentage changes, convert each change into a multiplier (e.g., +20% -> ×1.20, −15% -> ×0.85) and multiply them together.',
    'For reverse percentage, always divide the final/given value by the correct combined multiplier to recover the original value.',
    'In comparative problems (two people, two quantities), set up separate expressions for each and equate or compare them.',
    'For profit/loss with discount, work out the marked price and selling price step by step before computing the profit or loss percentage on the cost price.',
    'In overlap (Venn-style) problems, use: %(A or B) = %(A) + %(B) − %(A and B).',
    'Re-read multi-step questions carefully to identify exactly which quantity is being asked for, since intermediate values are often close to the answer options.'
  ]
};

export const PERCENTAGE_PDF_TA: PercentagePdfLesson = {
  lessonTitle: '1. சதவீதம்',
  objectivesTitle: '1. கற்றல் நோக்கங்கள்',
  objectivesPreamble: 'இப்பாடத்தை நிறைவு செய்த பின் கற்போர் பின்வருவனவற்றைச் செய்ய இயலும்:',
  objectives: [
    'சதவீதம், சதவீத அதிகரிப்பு மற்றும் சதவீதக் குறைவு ஆகியவற்றைத் துல்லியமாகக் கணக்கிடுதல்.',
    'தலைகீழ் சதவீதம் மற்றும் தொடர்ச்சியான சதவீத மாற்றம் தொடர்பான கணக்குகளைத் தீர்த்தல்.',
    'சதவீதக் கருத்துகளை அன்றாட வாழ்க்கை மற்றும் தேர்வுச் சூழல்களில் (இலாபம்-நட்டம், மக்கள்தொகை, தள்ளுபடி, கலவைகள்) பயன்படுத்துதல்.',
    'போட்டித் தேர்வுத் தரத்திலான, பல படிநிலைச் சதவீதக் கணக்குகளைத் திறம்படத் தீர்த்தல்.'
  ],
  overviewTitle: '2. பாடக் கண்ணோட்டம்',
  overview:
    'TNPSC குரூப் 1 போன்ற போட்டித் தேர்வுகளில் மிக அடிப்படையானதும் அடிக்கடி கேட்கப்படுவதுமான தலைப்புகளில் சதவீதம் ஒன்றாகும். இலாபம் மற்றும் நட்டம், தள்ளுபடி, மக்கள்தொகை வளர்ச்சி, தரவு விளக்கம், தனிவட்டி ஆகிய கணக்குகளுக்குச் சதவீதமே அடிப்படையாக அமைகிறது. இத்திருத்திய பாடம் எளிய ஒருபடி சூத்திர நினைவுகூர்தலுக்குப் பதிலாக, உயர்நிலை, பல படிநிலைச் சிக்கல் தீர்த்தலுக்கு -- தொடர்ச்சியான சதவீத மாற்றங்கள், தலைகீழ் சதவீதம், ஒப்பீட்டு மற்றும் மேற்பொருந்துதல் (வென் படம் வகை) கணக்குகளுக்கு -- முக்கியத்துவம் அளிக்கிறது.',
  conceptTitle: '3. கருத்து விளக்கம்',
  examInsightTitle: '3.1 தேர்வு நோக்கு',
  examInsight:
    "TNPSC குரூப் 1 மற்றும் இதுபோன்ற போட்டித் தேர்வுகளில், சதவீத வினாக்கள் வெறும் 'Y-இல் X % காண்க' என்ற எளிய கணக்காக அமைவது அரிது. அவை பொதுவாக இரண்டு அல்லது அதற்கு மேற்பட்ட நிபந்தனைகளை -- தொடர்ச்சியான மாற்றங்கள், வித்தியாசம் அல்லது வேறுபாடு, தொடர்புடைய இரண்டு அளவுகள், அல்லது வகைகளுக்கு இடையிலான மேற்பொருந்துதல் -- இணைக்கின்றன; தீர்ப்பதற்கு முன் தேர்வர் ஓர் உறவை அமைக்க வேண்டியுள்ளது. இப்பாடத்தின் வினாக்கள் அந்த தரத்தில் அமைக்கப்பட்டுள்ளன: ஒவ்வொரு வினாவும் ஒரே ஒரு மதிப்பைப் பிரதியிடுவதாக இல்லாமல், குறைந்தது இரண்டு தர்க்கப் படிநிலைகளைக் கோருகிறது.",
  coreConceptsTitle: '3.2 அடிப்படைக் கருத்துகள்',
  coreConceptsIntro:
    'சதவீதம் என்பது ஒரு பகுதியை முழுமையுடன் ஒப்பிட்டு, 100-க்கு எவ்வளவு என வெளிப்படுத்துவதாகும். போட்டித் தேர்வுகளில் கற்போர் பின்வருவனவற்றில் தேர்ச்சி பெற்றிருக்க வேண்டும்:',
  coreConcepts: [
    'பின்னங்கள், தசமங்கள், சதவீதங்கள் ஆகியவற்றுக்கிடையே மாற்றுதல் மற்றும் கொடுக்கப்பட்ட அளவின் சதவீதத்தைக் காணுதல்.',
    'தலைகீழ் சதவீதம் (மூல மதிப்பைக் காணுதல்) உட்பட, சதவீத அதிகரிப்பு மற்றும் சதவீதக் குறைவைக் கணக்கிடுதல்.',
    'தொடர்ச்சியான சதவீத மாற்றங்களை (ஒன்றன்பின் ஒன்றாகச் செய்யப்படும் இரண்டு அல்லது அதற்கு மேற்பட்ட மாற்றங்கள்) பெருக்கக் காரணிகள் மூலம் சரியாகப் பயன்படுத்துதல்.',
    'சதவீதப் புள்ளிகளில் ஏற்படும் மாற்றத்தையும், அடிப்படை அளவில் ஏற்படும் சதவீத (சார்பு) மாற்றத்தையும் வேறுபடுத்தி அறிதல்.',
    'ஒப்பீட்டுச் சதவீதக் கணக்குகளைத் தீர்த்தல் (எ.கா., இரண்டு தேர்வர்கள், வருமானம் மற்றும் செலவு போன்ற தொடர்புடைய இரண்டு அளவுகள்).',
    'இலாபம் மற்றும் நட்டம், தொடர்ச்சியான தள்ளுபடிகள், கலவைகள்/செறிவுகள், பல காலங்களுக்கான மக்கள்தொகை அல்லது தேய்மானம் ஆகியவற்றில் சதவீதத்தைப் பயன்படுத்துதல்.',
    'இரண்டு வகைகளும் அவற்றின் வெட்டும் (பொதுப்) பகுதியும் அடங்கிய மேற்பொருந்துதல் (வென் படம் வகை) சதவீதக் கணக்குகளைத் தீர்த்தல்.'
  ],
  commonMistakesTitle: '3.3 பொதுவான தவறுகள்',
  commonMistakes: [
    'தொடர்புடைய காரணிகளைப் பெருக்குவதற்குப் பதிலாக, தொடர்ச்சியான சதவீத மாற்றங்களை நேரடியாகக் கூட்டுதல் அல்லது கழித்தல்.',
    'சதவீதப் புள்ளி மாற்றத்தையும் சதவீத (சார்பு) அதிகரிப்பு அல்லது குறைவையும் குழப்பிக்கொள்ளுதல்.',
    'தள்ளுபடி அல்லது இலாபச் சதவீதத்தைத் தவறான அடிப்படையில் (குறித்த விலை / அடக்க விலை / விற்பனை விலை) பயன்படுத்துதல்.',
    'தலைகீழ் சதவீதக் கணக்குகளில், சரியான பெருக்கக் காரணியால் வகுப்பதற்குப் பதிலாகச் சதவீத மதிப்பாலேயே வகுத்தல்.',
    'மேற்பொருந்துதல் (வென் படம் வகை) கணக்குகளில், இரண்டு சதவீதங்களை இணைக்கும்போது பொதுப் பகுதியைக் கணக்கில் கொள்ள மறத்தல்.'
  ],
  examTipsTitle: '3.4 தேர்வுக் குறிப்புகள்',
  examTips: [
    'தொடர்ச்சியான சதவீத மாற்றங்களுக்கு, ஒவ்வொரு மாற்றத்தையும் பெருக்கக் காரணியாக மாற்றி (எ.கா., +20% -> ×1.20, −15% -> ×0.85) அவற்றை ஒன்றாகப் பெருக்கவும்.',
    'தலைகீழ் சதவீதத்தில், மூல மதிப்பைப் பெற இறுதி/கொடுக்கப்பட்ட மதிப்பைச் சரியான ஒருங்கிணைந்த பெருக்கக் காரணியால் எப்போதும் வகுக்கவும்.',
    'ஒப்பீட்டுக் கணக்குகளில் (இரண்டு நபர்கள், இரண்டு அளவுகள்), ஒவ்வொன்றுக்கும் தனித்தனிக் கோவைகளை அமைத்து, அவற்றைச் சமப்படுத்தவும் அல்லது ஒப்பிடவும்.',
    'தள்ளுபடியுடன் கூடிய இலாப/நட்டக் கணக்குகளில், அடக்க விலையின் மீது இலாப அல்லது நட்டச் சதவீதத்தைக் கணக்கிடும் முன், குறித்த விலை மற்றும் விற்பனை விலையைப் படிப்படியாகக் கண்டறியவும்.',
    'மேற்பொருந்துதல் (வென் படம் வகை) கணக்குகளில் பயன்படுத்தவும்: %(A அல்லது B) = %(A) + %(B) − %(A மற்றும் B).',
    'இடைநிலை மதிப்புகள் பெரும்பாலும் விடைத் தேர்வுகளுக்கு நெருக்கமாக இருப்பதால், எந்த அளவு கேட்கப்படுகிறது என்பதைத் துல்லியமாக அறியப் பல படிநிலை வினாக்களைக் கவனமாக மீண்டும் படிக்கவும்.'
  ]
};
