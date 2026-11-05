export interface ReflectionQuestionDef {
  number: number;
  question: string;
  question_ta?: string;
  options: string[];
  options_ta?: string[];
}

export const PERCENTAGE_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of multi-step percentage question did you find most challenging?',
    question_ta: 'எந்த வகைப் பல படிநிலைச் சதவீத வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Successive percentage changes (two or more steps)',
      'Reverse percentage (finding the original value)',
      'Comparative two-quantity or two-candidate problems',
      'Overlap (Venn-style) or mixture/concentration problems',
    ],
    options_ta: [
      'தொடர்ச்சியான சதவீத மாற்றங்கள் (இரண்டு அல்லது அதற்கு மேற்பட்ட படிநிலைகள்)',
      'தலைகீழ் சதவீதம் (மூல மதிப்பைக் காணுதல்)',
      'இரண்டு அளவுகள் அல்லது இரண்டு தேர்வர்களை ஒப்பிடும் கணக்குகள்',
      'மேற்பொருந்துதல் (வென் படம் வகை) அல்லது கலவை/செறிவுக் கணக்குகள்',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you solve multi-step percentage problems more efficiently?',
    question_ta: 'பல படிநிலைச் சதவீதக் கணக்குகளை மிகத் திறம்படத் தீர்க்க எந்த உத்தி உதவியது?',
    options: [
      'Converting each percentage change into a multiplying factor',
      'Assuming the original value as 100 and tracking the change',
      'Setting up separate equations for each condition given',
      'Breaking the problem into smaller, labelled steps',
    ],
    options_ta: [
      'ஒவ்வொரு சதவீத மாற்றத்தையும் பெருக்கக் காரணியாக மாற்றுதல்',
      'மூல மதிப்பை 100 எனக் கொண்டு மாற்றத்தைப் பின்தொடர்தல்',
      'கொடுக்கப்பட்ட ஒவ்வொரு நிபந்தனைக்கும் தனிச் சமன்பாடுகளை அமைத்தல்',
      'கணக்கைச் சிறிய, பெயரிடப்பட்ட படிநிலைகளாகப் பிரித்தல்',
    ],
  },
  {
    number: 3,
    question: 'While solving a multi-step percentage problem, I usually…',
    question_ta: 'பல படிநிலைச் சதவீதக் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Identify every condition in the question before calculating anything',
      'Start calculating from the first number I see',
      'Guess the answer using the options',
      'Re-read the question after solving, to check I answered what was asked',
    ],
    options_ta: [
      'எதையும் கணக்கிடும் முன் வினாவிலுள்ள ஒவ்வொரு நிபந்தனையையும் அடையாளம் காண்கிறேன்',
      'நான் முதலில் பார்க்கும் எண்ணிலிருந்தே கணக்கிடத் தொடங்குகிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'கேட்கப்பட்டதற்கே விடையளித்தேனா எனச் சரிபார்க்க, தீர்த்த பின் வினாவை மீண்டும் படிக்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Setting up the correct relationship from a word problem',
      'Conceptual understanding of successive/reverse percentage',
      'Calculation accuracy in multi-step problems',
      'Time management on longer, multi-step questions',
    ],
    options_ta: [
      'சொற்கணக்கிலிருந்து சரியான உறவை அமைத்தல்',
      'தொடர்ச்சியான/தலைகீழ் சதவீதம் பற்றிய கருத்தியல் புரிதல்',
      'பல படிநிலைக் கணக்குகளில் கணக்கீட்டுத் துல்லியம்',
      'நீண்ட, பல படிநிலை வினாக்களில் நேர மேலாண்மை',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, I monitored my mistakes by…',
    question_ta: 'இப்பாடத்தின்போது, நான் என் தவறுகளைக் கண்காணித்த முறை...',
    options: [
      'Checking each step of a multi-step solution, not just the final answer',
      'Comparing my method with the given solution',
      'Reviewing incorrect answers to find where the setup went wrong',
      'Re-attempting the problem with a fresh equation',
    ],
    options_ta: [
      'இறுதி விடையை மட்டுமல்லாமல், பல படிநிலைத் தீர்வின் ஒவ்வொரு படியையும் சரிபார்த்தல்',
      'என் முறையைக் கொடுக்கப்பட்ட தீர்வுடன் ஒப்பிடுதல்',
      'அமைப்பில் எங்கே தவறு நேர்ந்தது எனக் கண்டறியத் தவறான விடைகளை மறுஆய்வு செய்தல்',
      'புதிய சமன்பாட்டுடன் கணக்கை மீண்டும் முயற்சித்தல்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step percentage problems?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், பல படிநிலைச் சதவீதக் கணக்குகளைத் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவு நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export const DEFAULT_COURSE_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of problem or concept did you find most challenging in this lesson?',
    options: [
      'Complex multi-step problems requiring multiple concepts',
      'Word problems and translating verbal statements into equations',
      'Questions involving calculations with time constraints',
      'Advanced variations and special case formulas',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you understand and solve problems most effectively?',
    options: [
      'Working through the step-by-step formulas and derivation',
      'Using shortcut methods and multiplying factors',
      'Visualizing the problem with diagrams and smaller steps',
      'Reviewing worked model examples and explanations',
    ],
  },
  {
    number: 3,
    question: 'While approaching a new problem in this topic, I usually…',
    options: [
      'Identify every given condition and requirement before calculating',
      'Start calculating immediately from the first values given',
      'Eliminate unlikely options before attempting the solution',
      'Re-verify calculations and ensure the question requirement was answered',
    ],
  },
  {
    number: 4,
    question: 'Which aspect of your problem-solving needs the most improvement?',
    options: [
      'Conceptual understanding of the fundamental principles',
      'Speed and calculation accuracy under time pressure',
      'Translating complex problem statements into mathematical expressions',
      'Memorizing and applying relevant formulas quickly',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, I monitored my mistakes by…',
    options: [
      'Checking each step of the solution, not just the final outcome',
      'Comparing my thought process with the provided detailed solution',
      'Re-attempting missed questions to discover where the error occurred',
      'Taking notes of tricky patterns and common pitfalls',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in this topic?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
  },
];

export const LOGICAL_REASONING_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of multi-step Logical Reasoning question did you find most challenging?',
    question_ta: 'எந்த வகைப் பல படிநிலைத் தருக்கக் காரணவியல் வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Multi-generation blood relation problems',
      'Direction problems requiring the Pythagorean relationship',
      'Two-conclusion syllogisms',
      'Multi-condition seating arrangement or stacking puzzles',
    ],
    options_ta: [
      'பல தலைமுறை இரத்த உறவுக் கணக்குகள்',
      'பிதாகரஸ் தொடர்பு தேவைப்படும் திசைக் கணக்குகள்',
      'இரு முடிவுகள் கொண்ட தருக்க வினாக்கள்',
      'பல நிபந்தனை இருக்கை அமைப்பு அல்லது அடுக்கு புதிர்கள்',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you solve multi-step Logical Reasoning problems more efficiently?',
    question_ta: 'பல படிநிலைத் தருக்கக் காரணவியல் கணக்குகளை மிகத் திறம்படத் தீர்க்க எந்த உத்தி உதவியது?',
    options: [
      'Drawing a quick family tree or diagram before answering',
      'Verifying the coding/series pattern against the full given example first',
      'Testing each syllogism conclusion against the valid logical rules',
      'Fixing the most specific constraint first in seating/ranking puzzles',
    ],
    options_ta: [
      'விடையளிக்கும் முன் விரைவான குடும்ப மரம் அல்லது வரைபடம் வரைதல்',
      'குறியீட்டு/தொடர் அமைப்பை முதலில் கொடுக்கப்பட்ட முழு எடுத்துக்காட்டுடன் சரிபார்த்தல்',
      'ஒவ்வொரு தருக்க முடிவையும் செல்லத்தக்க விதிகளுடன் சோதித்தல்',
      'இருக்கை/தரவரிசைப் புதிர்களில் மிகக் குறிப்பிட்ட நிபந்தனையை முதலில் நிலைநிறுத்துதல்',
    ],
  },
  {
    number: 3,
    question: 'While solving a multi-step Logical Reasoning problem, I usually…',
    question_ta: 'பல படிநிலைத் தருக்கக் காரணவியல் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Focus closely on every clue before drawing any conclusion',
      'Start answering based on the first clue I read',
      'Guess the answer using the options',
      'Re-read the question after solving, to check I answered what was asked',
    ],
    options_ta: [
      'எந்த முடிவுக்கும் வரும் முன் ஒவ்வொரு குறிப்பிலும் நெருக்கமாகக் கவனம் செலுத்துகிறேன்',
      'நான் படிக்கும் முதல் குறிப்பின் அடிப்படையிலேயே விடையளிக்கத் தொடங்குகிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'கேட்கப்பட்டதற்கே விடையளித்தேனா எனச் சரிபார்க்க, தீர்த்த பின் வினாவை மீண்டும் படிக்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Tracking multi-generation blood relations accurately',
      'Distinguishing valid from invalid syllogism conclusions',
      'Attention to detail when reading directional or positional clues',
      'Systematically placing all elements in seating/ranking puzzles',
    ],
    options_ta: [
      'பல தலைமுறை இரத்த உறவுகளைத் துல்லியமாகப் பின்தொடர்தல்',
      'செல்லத்தக்க மற்றும் செல்லாத தருக்க முடிவுகளை வேறுபடுத்துதல்',
      'திசை அல்லது இடக் குறிப்புகளைப் படிக்கும்போது நுணுக்கமான கவனம்',
      'இருக்கை/தரவரிசைப் புதிர்களில் அனைவரையும் முறையாக அமர்த்துதல்',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, when I got stuck on a problem, I usually…',
    question_ta: 'இப்பாடத்தின்போது, ஒரு கணக்கில் சிக்கிக்கொண்டபோது, நான் வழக்கமாக...',
    options: [
      'Re-read the clues carefully and tried again on my own',
      'Checked the solution and worked backward to understand my error',
      'Sought help or clarification when a concept was still unclear afterward',
      'Moved on and returned to the problem later with a fresh approach',
    ],
    options_ta: [
      'குறிப்புகளைக் கவனமாக மீண்டும் படித்து, நானே மீண்டும் முயன்றேன்',
      'தீர்வைப் பார்த்துப் பின்னோக்கிச் செயல்பட்டு என் தவறைப் புரிந்துகொண்டேன்',
      'அதன் பின்னும் ஒரு கருத்து தெளிவில்லாதபோது உதவி அல்லது விளக்கம் நாடினேன்',
      'அடுத்த கணக்குக்குச் சென்று, பின்னர் புதிய அணுகுமுறையுடன் திரும்பி வந்தேன்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step, TNPSC Group 1-standard Logical Reasoning questions?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், TNPSC குரூப் 1 தரத்திலான பல படிநிலைத் தருக்கக் காரணவியல் வினாக்களைத் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவு நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export const RATIO_AND_PROPORTION_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of multi-step ratio and proportion question did you find most challenging?',
    question_ta: 'எந்த வகைப் பல படிநிலை விகிதம் மற்றும் விகிதசம வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Partnership with time-weighted capital or a partner joining later',
      'Ratio changes after a fixed value is added or subtracted',
      'Age, mixture, or map-scale application problems',
      'Comparative (set-overlap) or reverse-engineering problems',
    ],
    options_ta: [
      'கால அடிப்படையிலான முதலீடு அல்லது பின்னர் சேரும் கூட்டாளி கொண்ட கூட்டாண்மை',
      'ஒரு நிலையான மதிப்பு கூட்டப்பட்ட அல்லது கழிக்கப்பட்ட பின் விகித மாற்றங்கள்',
      'வயது, கலவை அல்லது வரைபட அளவுகோல் பயன்பாட்டுக் கணக்குகள்',
      'ஒப்பீட்டு (கண மேற்பொருந்துதல்) அல்லது பின்னோக்கித் தீர்க்கும் கணக்குகள்',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you solve multi-step ratio and proportion problems more efficiently?',
    question_ta: 'பல படிநிலை விகிதம் மற்றும் விகிதசமக் கணக்குகளை மிகத் திறம்படத் தீர்க்க எந்த உத்தி உதவியது?',
    options: [
      'Assuming a variable multiplier (x or k) and forming an equation',
      'Equalising the common term across two ratios before combining them',
      'Working backward from the answer options',
      'Breaking the problem into smaller, labelled steps',
    ],
    options_ta: [
      'ஒரு மாறிப் பெருக்கியை (x அல்லது k) கொண்டு சமன்பாட்டை அமைத்தல்',
      'இணைக்கும் முன் இரண்டு விகிதங்களிலும் பொது உறுப்பைச் சமமாக்குதல்',
      'விடைத் தேர்வுகளிலிருந்து பின்னோக்கிச் செயல்படுதல்',
      'கணக்கைச் சிறிய, பெயரிடப்பட்ட படிநிலைகளாகப் பிரித்தல்',
    ],
  },
  {
    number: 3,
    question: 'While solving a multi-step ratio and proportion problem, I usually…',
    question_ta: 'பல படிநிலை விகிதம் மற்றும் விகிதசமக் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Identify every condition in the question before writing any equation',
      'Start calculating from the first number I see',
      'Guess the answer using the options',
      'Re-read the question after solving, to check I answered what was asked',
    ],
    options_ta: [
      'எந்தச் சமன்பாட்டையும் எழுதும் முன் வினாவிலுள்ள ஒவ்வொரு நிபந்தனையையும் அடையாளம் காண்கிறேன்',
      'நான் முதலில் பார்க்கும் எண்ணிலிருந்தே கணக்கிடத் தொடங்குகிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'கேட்கப்பட்டதற்கே விடையளித்தேனா எனச் சரிபார்க்க, தீர்த்த பின் வினாவை மீண்டும் படிக்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Setting up the correct equation from a word problem',
      'Conceptual understanding of proportion types (direct/inverse/joint)',
      'Calculation accuracy in multi-step problems',
      'Time management on longer, multi-step questions',
    ],
    options_ta: [
      'சொற்கணக்கிலிருந்து சரியான சமன்பாட்டை அமைத்தல்',
      'விகிதசம வகைகள் (நேர்/எதிர்/கூட்டு) பற்றிய கருத்தியல் புரிதல்',
      'பல படிநிலைக் கணக்குகளில் கணக்கீட்டுத் துல்லியம்',
      'நீண்ட, பல படிநிலை வினாக்களில் நேர மேலாண்மை',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, I monitored my mistakes by…',
    question_ta: 'இப்பாடத்தின்போது, நான் என் தவறுகளைக் கண்காணித்த முறை...',
    options: [
      'Checking each step of a multi-step solution, not just the final answer',
      'Comparing my method with the given solution',
      'Reviewing incorrect answers to find where the setup went wrong',
      'Re-attempting the problem with a fresh equation',
    ],
    options_ta: [
      'இறுதி விடையை மட்டுமல்லாமல், பல படிநிலைத் தீர்வின் ஒவ்வொரு படியையும் சரிபார்த்தல்',
      'என் முறையைக் கொடுக்கப்பட்ட தீர்வுடன் ஒப்பிடுதல்',
      'அமைப்பில் எங்கே தவறு நேர்ந்தது எனக் கண்டறியத் தவறான விடைகளை மறுஆய்வு செய்தல்',
      'புதிய சமன்பாட்டுடன் கணக்கை மீண்டும் முயற்சித்தல்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step, TNPSC standard ratio and proportion questions?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், TNPSC தரத்திலான பல படிநிலை விகிதம் மற்றும் விகிதசம வினாக்களைத் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவு நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export const TIME_AND_WORK_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of multi-step Time and Work question did you find most challenging?',
    question_ta: 'எந்த வகைப் பல படிநிலைக் காலம் மற்றும் வேலை வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Combined work with a worker leaving or joining midway',
      'Alternate-day work problems',
      'Pipes and cisterns (inlet and outlet together)',
      'Wage-sharing based on efficiency ratio',
    ],
    options_ta: [
      'இடையில் பணியாளர் விலகும் அல்லது சேரும் ஒருங்கிணைந்த வேலை',
      'மாற்று நாள் வேலைக் கணக்குகள்',
      'குழாய்களும் தொட்டிகளும் (நிரப்பும் மற்றும் வெளியேற்றும் குழாய்கள் ஒன்றாக)',
      'திறன் விகித அடிப்படையிலான கூலிப் பகிர்வு',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you solve multi-step Time and Work problems more efficiently?',
    question_ta: 'பல படிநிலைக் காலம் மற்றும் வேலைக் கணக்குகளை மிகத் திறம்படத் தீர்க்க எந்த உத்தி உதவியது?',
    options: [
      'Using the LCM (unit-work) method instead of fractions',
      'Converting efficiency percentages/ratios into time ratios first',
      'Tracking work completed as a running fraction',
      'Restating what the question was actually asking before calculating',
    ],
    options_ta: [
      'பின்னங்களுக்குப் பதிலாக மீ.பொ.ம (அலகு-வேலை) முறையைப் பயன்படுத்துதல்',
      'திறன் சதவீதங்கள்/விகிதங்களை முதலில் கால விகிதங்களாக மாற்றுதல்',
      'முடிக்கப்பட்ட வேலையைத் தொடர் பின்னமாகக் கண்காணித்தல்',
      'கணக்கிடும் முன் வினா உண்மையில் என்ன கேட்கிறது என்பதை மீண்டும் கூறிக்கொள்ளுதல்',
    ],
  },
  {
    number: 3,
    question: 'While solving a multi-step Time and Work problem, I usually…',
    question_ta: 'பல படிநிலைக் காலம் மற்றும் வேலைக் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Identify every condition in the question before calculating anything',
      'Start calculating from the first number I see',
      'Guess the answer using the options',
      'Re-read the question after solving, to check I answered what was asked',
    ],
    options_ta: [
      'எதையும் கணக்கிடும் முன் வினாவிலுள்ள ஒவ்வொரு நிபந்தனையையும் அடையாளம் காண்கிறேன்',
      'நான் முதலில் பார்க்கும் எண்ணிலிருந்தே கணக்கிடத் தொடங்குகிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'கேட்கப்பட்டதற்கே விடையளித்தேனா எனச் சரிபார்க்க, தீர்த்த பின் வினாவை மீண்டும் படிக்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Setting up the correct relationship from a word problem',
      'Applying the LCM/unit-work method efficiently',
      'Calculation accuracy in multi-step problems',
      'Time management on longer, multi-step questions',
    ],
    options_ta: [
      'சொற்கணக்கிலிருந்து சரியான தொடர்பை அமைத்தல்',
      'மீ.பொ.ம/அலகு-வேலை முறையைத் திறம்படப் பயன்படுத்துதல்',
      'பல படிநிலைக் கணக்குகளில் கணக்கீட்டுத் துல்லியம்',
      'நீண்ட, பல படிநிலை வினாக்களில் நேர மேலாண்மை',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, I monitored my mistakes by…',
    question_ta: 'இப்பாடத்தின்போது, நான் என் தவறுகளைக் கண்காணித்த முறை...',
    options: [
      'Checking each step of a multi-step solution, not just the final answer',
      'Comparing my method with the given solution',
      'Reviewing incorrect answers to find where the setup went wrong',
      'Re-attempting the problem with a fresh equation',
    ],
    options_ta: [
      'இறுதி விடையை மட்டுமல்லாமல், பல படிநிலைத் தீர்வின் ஒவ்வொரு படியையும் சரிபார்த்தல்',
      'என் முறையைக் கொடுக்கப்பட்ட தீர்வுடன் ஒப்பிடுதல்',
      'அமைப்பில் எங்கே தவறு நேர்ந்தது எனக் கண்டறியத் தவறான விடைகளை மறுஆய்வு செய்தல்',
      'புதிய சமன்பாட்டுடன் கணக்கை மீண்டும் முயற்சித்தல்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step, TNPSC standard Time and Work questions?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், TNPSC தரத்திலான பல படிநிலைக் காலம் மற்றும் வேலை வினாக்களைத் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவு நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export const AREA_AND_VOLUME_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of multi-step Area and Volume question did you find most challenging?',
    question_ta: 'எந்த வகைப் பல படிநிலைப் பரப்பளவு மற்றும் கன அளவு வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Composite figures (path around a field, embankment around a well)',
      'Melting-and-recasting or liquid-transfer problems',
      'Scale-factor (ratio of areas/volumes) problems',
      'Cost-based problems (fencing, whitewashing, fabric for a tent)',
    ],
    options_ta: [
      'கூட்டு உருவங்கள் (வயலைச் சுற்றிய பாதை, கிணற்றைச் சுற்றிய கரை)',
      'உருக்கி மறுவார்ப்பு அல்லது திரவ மாற்றக் கணக்குகள்',
      'அளவுமாற்றக் காரணி (பரப்பளவு/கன அளவு விகிதம்) கணக்குகள்',
      'செலவு சார்ந்த கணக்குகள் (வேலி அமைத்தல், வெள்ளையடித்தல், கூடாரத்திற்கான துணி)',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you solve multi-step Area and Volume problems more efficiently?',
    question_ta: 'பல படிநிலைப் பரப்பளவு மற்றும் கன அளவுக் கணக்குகளை மிகத் திறம்படத் தீர்க்க எந்த உத்தி உதவியது?',
    options: [
      'Restating exactly what was asked (area, volume, CSA, or TSA) before calculating',
      'Computing outer and inner regions separately in composite-figure problems',
      'Equating volumes directly in melting-and-recasting problems',
      'Applying k² and k³ directly in scale-factor problems',
    ],
    options_ta: [
      'கணக்கிடும் முன் கேட்கப்பட்டது (பரப்பளவு, கன அளவு, வளைபரப்பு, அல்லது மொத்தப் புறப்பரப்பு) எது என்பதைத் துல்லியமாக மீண்டும் கூறிக்கொள்ளுதல்',
      'கூட்டு உருவக் கணக்குகளில் வெளி மற்றும் உள் பகுதிகளைத் தனித்தனியாகக் கணக்கிடுதல்',
      'உருக்கி மறுவார்ப்புக் கணக்குகளில் கன அளவுகளை நேரடியாகச் சமப்படுத்துதல்',
      'அளவுமாற்றக் காரணிக் கணக்குகளில் k² மற்றும் k³ ஐ நேரடியாகப் பயன்படுத்துதல்',
    ],
  },
  {
    number: 3,
    question: 'While solving a multi-step Area and Volume problem, I usually…',
    question_ta: 'பல படிநிலைப் பரப்பளவு மற்றும் கன அளவுக் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Identify every condition and figure involved before calculating anything',
      'Start calculating from the first number I see',
      'Guess the answer using the options',
      'Re-read the question after solving, to check I answered what was asked',
    ],
    options_ta: [
      'எதையும் கணக்கிடும் முன் தொடர்புடைய ஒவ்வொரு நிபந்தனையையும் உருவத்தையும் அடையாளம் காண்கிறேன்',
      'நான் முதலில் பார்க்கும் எண்ணிலிருந்தே கணக்கிடத் தொடங்குகிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'கேட்கப்பட்டதற்கே விடையளித்தேனா எனச் சரிபார்க்க, தீர்த்த பின் வினாவை மீண்டும் படிக்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Distinguishing curved surface area from total surface area',
      'Setting up the correct relationship in composite-figure problems',
      'Calculation accuracy in multi-step problems',
      'Attention to detail when reading given measurements (radius vs. diameter, height vs. slant height)',
    ],
    options_ta: [
      'வளைபரப்பையும் மொத்தப் புறப்பரப்பையும் வேறுபடுத்துதல்',
      'கூட்டு உருவக் கணக்குகளில் சரியான தொடர்பை அமைத்தல்',
      'பல படிநிலைக் கணக்குகளில் கணக்கீட்டுத் துல்லியம்',
      'கொடுக்கப்பட்ட அளவுகளைப் படிக்கும்போது நுணுக்கமான கவனம் (ஆரம் / விட்டம், உயரம் / சாயுயரம்)',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, I monitored my mistakes by…',
    question_ta: 'இப்பாடத்தின்போது, நான் என் தவறுகளைக் கண்காணித்த முறை...',
    options: [
      'Checking each step of a multi-step solution, not just the final answer',
      'Comparing my method with the given solution',
      'Reviewing incorrect answers to find where the setup went wrong',
      'Re-attempting the problem with a fresh diagram or equation',
    ],
    options_ta: [
      'இறுதி விடையை மட்டுமல்லாமல், பல படிநிலைத் தீர்வின் ஒவ்வொரு படியையும் சரிபார்த்தல்',
      'என் முறையைக் கொடுக்கப்பட்ட தீர்வுடன் ஒப்பிடுதல்',
      'அமைப்பில் எங்கே தவறு நேர்ந்தது எனக் கண்டறியத் தவறான விடைகளை மறுஆய்வு செய்தல்',
      'புதிய வரைபடம் அல்லது சமன்பாட்டுடன் கணக்கை மீண்டும் முயற்சித்தல்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step, TNPSC standard Area and Volume questions?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், TNPSC தரத்திலான பல படிநிலைப் பரப்பளவு மற்றும் கன அளவு வினாக்களைத் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவு நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export const NUMBER_SERIES_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of Number Series question did you find most challenging?',
    question_ta: 'எந்த வகை எண் தொடர் வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Series with an increasing or decreasing gap',
      'Alternating-operation series',
      'Two-interleaved series',
      'Wrong-number or missing middle-term identification',
    ],
    options_ta: [
      'அதிகரிக்கும் அல்லது குறையும் இடைவெளி கொண்ட தொடர்',
      'மாறி மாறி வரும் செயல் தொடர்',
      'இரு இடையிட்ட தொடர்',
      'தவறான எண் அல்லது நடுவில் விடுபட்ட உறுப்பை அடையாளம் காணுதல்',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you identify patterns more efficiently?',
    question_ta: 'அமைப்புகளை மிகத் திறம்பட அடையாளம் காண எந்த உத்தி உதவியது?',
    options: [
      'Writing out the row of differences between consecutive terms',
      'Splitting a two-interleaved series into odd-position and even-position sub-series',
      'Computing the fully expected series before checking for a wrong number',
      'Testing the simplest pattern (constant difference/ratio) before more complex ones',
    ],
    options_ta: [
      'அடுத்தடுத்த உறுப்புகளின் வித்தியாசங்களை வரிசையாக எழுதுதல்',
      'இரு இடையிட்ட தொடரை ஒற்றை இட மற்றும் இரட்டை இட உட்தொடர்களாகப் பிரித்தல்',
      'தவறான எண்ணைச் சரிபார்க்கும் முன் முழு எதிர்பார்க்கப்படும் தொடரைக் கணக்கிடுதல்',
      'சிக்கலான அமைப்புகளுக்கு முன் எளிய அமைப்பை (மாறா வித்தியாசம்/விகிதம்) சோதித்தல்',
    ],
  },
  {
    number: 3,
    question: 'While solving a Number Series problem, I usually…',
    question_ta: 'எண் தொடர் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Test the simplest pattern first, then move to more complex ones systematically',
      'Try to guess the pattern from just the first two terms',
      'Guess the answer using the options',
      'Verify my pattern against every term before finalising the answer',
    ],
    options_ta: [
      'முதலில் எளிய அமைப்பைச் சோதித்து, பின்னர் முறையாகச் சிக்கலானவற்றுக்குச் செல்கிறேன்',
      'முதல் இரண்டு உறுப்புகளை மட்டும் கொண்டு அமைப்பை ஊகிக்க முயல்கிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'விடையை இறுதி செய்யும் முன் என் அமைப்பை ஒவ்வோர் உறுப்புடனும் சரிபார்க்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Recognising square, cube, or prime-number series quickly',
      'Identifying the two operations in an alternating series',
      'Spotting the wrong term in a series accurately',
      'Verifying a missing middle term against both surrounding terms',
    ],
    options_ta: [
      'வர்க்க, கன, அல்லது பகா எண் தொடர்களை விரைவாக அடையாளம் காணுதல்',
      'மாறி மாறி வரும் தொடரில் இரு செயல்களையும் அடையாளம் காணுதல்',
      'தொடரில் உள்ள தவறான உறுப்பைத் துல்லியமாகக் கண்டறிதல்',
      'நடுவில் விடுபட்ட உறுப்பைச் சுற்றியுள்ள இரு உறுப்புகளுடனும் சரிபார்த்தல்',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, I monitored my accuracy by…',
    question_ta: 'இப்பாடத்தின்போது, நான் என் துல்லியத்தைக் கண்காணித்த முறை...',
    options: [
      'Checking my identified pattern against every term in the series, not just a few',
      'Comparing my method with the given solution',
      'Reviewing incorrect answers to find which pattern type I had missed',
      'Re-attempting the problem by testing a different pattern type',
    ],
    options_ta: [
      'நான் கண்டறிந்த அமைப்பைச் சில உறுப்புகளுடன் மட்டுமல்லாமல், தொடரின் ஒவ்வோர் உறுப்புடனும் சரிபார்த்தல்',
      'என் முறையைக் கொடுக்கப்பட்ட தீர்வுடன் ஒப்பிடுதல்',
      'நான் தவறவிட்ட அமைப்பு வகையைக் கண்டறியத் தவறான விடைகளை மறுஆய்வு செய்தல்',
      'வேறொரு அமைப்பு வகையைச் சோதித்துக் கணக்கை மீண்டும் முயற்சித்தல்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step, TNPSC standard Number Series questions?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், TNPSC தரத்திலான பல படிநிலை எண் தொடர் வினாக்களைத் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவு நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export const SIMPLIFICATION_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of Simplification question did you find most challenging?',
    question_ta: 'எந்த வகைச் சுருக்குதல் வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Multi-step BODMAS expressions with mixed operations',
      'Complex (nested) fractions',
      'Surds, indices, and recurring decimals',
      'Approximation problems',
    ],
    options_ta: [
      'கலப்புச் செயல்கள் கொண்ட பல படிநிலை BODMAS கோவைகள்',
      'சிக்கலான (உள்ளடங்கிய) பின்னங்கள்',
      'முறுடுகள், அடுக்குகள், சுழல் தசமங்கள்',
      'தோராயமாக்கல் கணக்குகள்',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you simplify multi-step expressions more efficiently?',
    question_ta: 'பல படிநிலைக் கோவைகளை மிகத் திறம்படச் சுருக்க எந்த உத்தி உதவியது?',
    options: [
      'Resolving brackets from the innermost outward before anything else',
      'Converting all fractions to a common denominator before combining',
      'Applying the laws of indices systematically (add/subtract exponents)',
      'Recognising shortcut identities (such as (a+b)²−(a−b)²=4ab)',
    ],
    options_ta: [
      'எதற்கும் முன் அடைப்புக்குறிகளை உள்ளார்ந்ததிலிருந்து வெளிநோக்கித் தீர்த்தல்',
      'இணைக்கும் முன் அனைத்துப் பின்னங்களையும் பொதுப் பகுதிக்கு மாற்றுதல்',
      'அடுக்கு விதிகளை முறையாகப் பயன்படுத்துதல் (அடுக்குகளைக் கூட்டுதல்/கழித்தல்)',
      'குறுக்கு வழி முற்றொருமைகளை அடையாளம் காணுதல் ((a+b)²−(a−b)²=4ab போன்றவை)',
    ],
  },
  {
    number: 3,
    question: 'While solving a multi-step Simplification problem, I usually…',
    question_ta: 'பல படிநிலைச் சுருக்குதல் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Follow BODMAS strictly, step by step, without skipping ahead',
      'Try to calculate the whole expression mentally in one go',
      'Guess the answer using the options',
      'Re-check my working after solving, to confirm I followed the correct order',
    ],
    options_ta: [
      'எந்தப் படியையும் தவிர்க்காமல், BODMAS-ஐப் படிப்படியாகக் கண்டிப்பாகப் பின்பற்றுகிறேன்',
      'முழுக் கோவையையும் ஒரே நேரத்தில் மனக்கணக்காகக் கணக்கிட முயல்கிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'சரியான வரிசையைப் பின்பற்றினேனா என உறுதிசெய்ய, தீர்த்த பின் என் செயல்முறையை மீண்டும் சரிபார்க்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Applying BODMAS consistently under time pressure',
      'Simplifying complex or nested fractions accurately',
      'Recognising surds, indices, and recurring-decimal shortcuts quickly',
      'Managing time across multiple calculation steps',
    ],
    options_ta: [
      'நேர அழுத்தத்தில் BODMAS-ஐச் சீராகப் பயன்படுத்துதல்',
      'சிக்கலான அல்லது உள்ளடங்கிய பின்னங்களைத் துல்லியமாகச் சுருக்குதல்',
      'முறுடுகள், அடுக்குகள், சுழல் தசமக் குறுக்கு வழிகளை விரைவாக அடையாளம் காணுதல்',
      'பல கணக்கீட்டுப் படிகளில் நேர மேலாண்மை',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, I monitored my accuracy by…',
    question_ta: 'இப்பாடத்தின்போது, நான் என் துல்லியத்தைக் கண்காணித்த முறை...',
    options: [
      'Re-checking each computation step, not just the final answer',
      'Comparing my method with the given solution',
      'Reviewing incorrect answers to find exactly where the order of operations went wrong',
      'Re-attempting the problem slowly, step by step, to catch the error',
    ],
    options_ta: [
      'இறுதி விடையை மட்டுமல்லாமல், ஒவ்வொரு கணக்கீட்டுப் படியையும் மீண்டும் சரிபார்த்தல்',
      'என் முறையைக் கொடுக்கப்பட்ட தீர்வுடன் ஒப்பிடுதல்',
      'செயல் வரிசை எங்கே தவறியது எனத் துல்லியமாகக் கண்டறியத் தவறான விடைகளை மறுஆய்வு செய்தல்',
      'பிழையைக் கண்டறிய, கணக்கை மெதுவாகப் படிப்படியாக மீண்டும் முயற்சித்தல்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step, TNPSC standard Simplification questions within time limits?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், TNPSC தரத்திலான பல படிநிலைச் சுருக்குதல் வினாக்களை நேர வரம்புக்குள் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவே நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export const PUZZLES_REFLECTION_QUESTIONS: ReflectionQuestionDef[] = [
  {
    number: 1,
    question: 'Which type of Puzzle question did you find most challenging?',
    question_ta: 'எந்த வகைப் புதிர் வினா உங்களுக்கு மிகவும் சவாலாக இருந்தது?',
    options: [
      'Circular or square seating arrangements',
      'Floor/building puzzles',
      'Scheduling puzzles (days or months)',
      'Age, ranking, or distribution puzzles',
    ],
    options_ta: [
      'வட்ட அல்லது சதுர இருக்கை அமைப்புகள்',
      'தளம்/கட்டடப் புதிர்கள்',
      'கால அட்டவணைப் புதிர்கள் (நாட்கள் அல்லது மாதங்கள்)',
      'வயது, தரவரிசை, அல்லது பகிர்வுப் புதிர்கள்',
    ],
  },
  {
    number: 2,
    question: 'Which strategy helped you solve multi-constraint puzzles more efficiently?',
    question_ta: 'பல நிபந்தனைப் புதிர்களை மிகத் திறம்படத் தீர்க்க எந்த உத்தி உதவியது?',
    options: [
      'Sketching the seating circle or floor list before answering',
      'Fixing the most specific clue first, then working outward',
      'Chaining all relative clues into a single ordered list',
      'Expressing every unknown in terms of one variable',
    ],
    options_ta: [
      'விடையளிக்கும் முன் இருக்கை வட்டம் அல்லது தளப் பட்டியலை வரைதல்',
      'மிகக் குறிப்பிட்ட குறிப்பை முதலில் நிலைநிறுத்தி, பின்னர் வெளிநோக்கிச் செயல்படுதல்',
      'அனைத்துச் சார்புக் குறிப்புகளையும் ஒரே வரிசைப் பட்டியலாக இணைத்தல்',
      'ஒவ்வொரு தெரியாத மதிப்பையும் ஒரே மாறியின் அடிப்படையில் வெளிப்படுத்துதல்',
    ],
  },
  {
    number: 3,
    question: 'While solving a multi-step Puzzle problem, I usually…',
    question_ta: 'பல படிநிலைப் புதிர்க் கணக்கைத் தீர்க்கும்போது, நான் வழக்கமாக...',
    options: [
      'Plan out a strategy for placing each clue before starting',
      'Try to solve it directly in my head without sketching anything',
      'Guess the answer using the options',
      'Re-check my arrangement against every clue after solving',
    ],
    options_ta: [
      'தொடங்கும் முன் ஒவ்வொரு குறிப்பையும் அமர்த்துவதற்கான உத்தியைத் திட்டமிடுகிறேன்',
      'எதையும் வரையாமல் நேரடியாக மனத்திலேயே தீர்க்க முயல்கிறேன்',
      'விடைத் தேர்வுகளைக் கொண்டு விடையை ஊகிக்கிறேன்',
      'தீர்த்த பின், என் அமைப்பை ஒவ்வொரு குறிப்புடனும் மீண்டும் சரிபார்க்கிறேன்',
    ],
  },
  {
    number: 4,
    question: 'Which aspect needs the most improvement?',
    question_ta: 'எந்த அம்சத்தில் அதிக முன்னேற்றம் தேவை?',
    options: [
      'Chaining multiple relative clues accurately',
      'Sketching circular/square seating arrangements correctly',
      'Attention to detail in floor and scheduling puzzles',
      'Setting up equations for age and distribution puzzles',
    ],
    options_ta: [
      'பல சார்புக் குறிப்புகளைத் துல்லியமாக இணைத்தல்',
      'வட்ட/சதுர இருக்கை அமைப்புகளைச் சரியாக வரைதல்',
      'தளம் மற்றும் கால அட்டவணைப் புதிர்களில் நுணுக்கமான கவனம்',
      'வயது மற்றும் பகிர்வுப் புதிர்களுக்குச் சமன்பாடுகளை அமைத்தல்',
    ],
  },
  {
    number: 5,
    question: 'During this lesson, when I got stuck on a puzzle, I usually…',
    question_ta: 'இப்பாடத்தின்போது, ஒரு புதிரில் சிக்கிக்கொண்டபோது, நான் வழக்கமாக...',
    options: [
      'Re-read all the clues carefully and tried again on my own',
      'Checked the solution and worked backward to understand my error',
      'Sought help or clarification when a concept was still unclear afterward',
      'Started over with a fresh sketch or a different starting clue',
    ],
    options_ta: [
      'அனைத்துக் குறிப்புகளையும் கவனமாக மீண்டும் படித்து, நானே மீண்டும் முயன்றேன்',
      'தீர்வைப் பார்த்துப் பின்னோக்கிச் செயல்பட்டு என் தவறைப் புரிந்துகொண்டேன்',
      'அதன் பின்னும் ஒரு கருத்து தெளிவில்லாதபோது உதவி அல்லது விளக்கம் நாடினேன்',
      'புதிய வரைபடத்துடன் அல்லது வேறு தொடக்கக் குறிப்புடன் மீண்டும் தொடங்கினேன்',
    ],
  },
  {
    number: 6,
    question: 'After completing this lesson, how confident are you in solving multi-step, TNPSC standard Puzzle questions?',
    question_ta: 'இப்பாடத்தை நிறைவு செய்த பின், TNPSC தரத்திலான பல படிநிலைப் புதிர் வினாக்களைத் தீர்ப்பதில் நீங்கள் எவ்வளவு நம்பிக்கையுடன் உள்ளீர்கள்?',
    options: [
      'Highly confident',
      'Moderately confident',
      'Slightly confident',
      'Need more practice',
    ],
    options_ta: [
      'மிகுந்த நம்பிக்கை',
      'மிதமான நம்பிக்கை',
      'சிறிதளவு நம்பிக்கை',
      'மேலும் பயிற்சி தேவை',
    ],
  },
];

export function getCourseReflectionQuestions(courseSlug: string, courseTitle?: string): ReflectionQuestionDef[] {
  const s = (courseSlug || '').toLowerCase();
  const t = (courseTitle || '').toLowerCase();

  if (
    s.includes('puzzle') ||
    t.includes('puzzle') ||
    t.includes('புதிர்')
  ) {
    return PUZZLES_REFLECTION_QUESTIONS;
  }

  if (
    s.includes('logical') ||
    s.includes('reasoning') ||
    t.includes('logical') ||
    t.includes('reasoning') ||
    t.includes('தருக்க') ||
    t.includes('காரணவியல்')
  ) {
    return LOGICAL_REASONING_REFLECTION_QUESTIONS;
  }

  if (
    s.includes('simplif') ||
    t.includes('simplif') ||
    t.includes('சுருக்குதல்')
  ) {
    return SIMPLIFICATION_REFLECTION_QUESTIONS;
  }

  if (
    s.includes('number') ||
    s.includes('series') ||
    t.includes('number') ||
    t.includes('series') ||
    t.includes('எண்') ||
    t.includes('தொடர்')
  ) {
    return NUMBER_SERIES_REFLECTION_QUESTIONS;
  }

  if (
    s.includes('area') ||
    s.includes('volume') ||
    t.includes('area') ||
    t.includes('volume') ||
    t.includes('பரப்பளவு') ||
    t.includes('கன அளவு')
  ) {
    return AREA_AND_VOLUME_REFLECTION_QUESTIONS;
  }

  if (
    s.includes('time') ||
    s.includes('work') ||
    t.includes('time') ||
    t.includes('work') ||
    t.includes('வேலை') ||
    t.includes('காலம்')
  ) {
    return TIME_AND_WORK_REFLECTION_QUESTIONS;
  }

  if (
    s.includes('ratio') ||
    s.includes('proportion') ||
    t.includes('ratio') ||
    t.includes('proportion') ||
    t.includes('விகிதம்') ||
    t.includes('விகிதசமம்')
  ) {
    return RATIO_AND_PROPORTION_REFLECTION_QUESTIONS;
  }

  if (s.includes('percent') || t.includes('percent') || t.includes('சதவீதம்')) {
    return PERCENTAGE_REFLECTION_QUESTIONS;
  }

  return DEFAULT_COURSE_REFLECTION_QUESTIONS;
}

