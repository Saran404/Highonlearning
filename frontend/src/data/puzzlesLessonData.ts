/** Exact Puzzles Lesson Theory extracted directly from Puzzlesenglish and Puzzlestamil PDFs. */
import type { LessonPdfData } from './ratioLessonData';

export const PUZZLES_PDF_EN: LessonPdfData = {
  lessonTitle: '8. Puzzles',
  objectivesTitle: '1. Learning Objectives',
  objectivesPreamble: 'The learner will be able to:',
  objectives: [
    'Solve circular and square seating arrangement puzzles involving multiple positional constraints.',
    'Solve floor/building, scheduling (day and month), and distribution puzzles systematically.',
    'Solve age-comparison and ranking puzzles involving multiple relative clues.',
    'Solve multi-step, competitive-examination-standard Puzzle questions efficiently, using Strategic Planning, Attention Control, Help-Seeking, and Self-Evaluation & Reflection.'
  ],
  overviewTitle: '2. Lesson Overview',
  overview:
    'Puzzles is a core Problem-Solving Skills topic in TNPSC Group 1 and allied competitive examinations, testing a candidate’s ability to analyse complex situations, identify relationships among multiple elements, formulate a solution strategy, and arrive at logical conclusions through systematic reasoning. This lesson emphasises higher-order, multi-constraint problem solving – circular seating with alternating genders, multi-floor buildings, scheduling across days and months, and distribution and ranking puzzles – rather than single-clue recall.',
  conceptTitle: '3. Concept Explanation',
  examInsightTitle: '3.1 Exam Insight',
  examInsight:
    'In TNPSC Group 1 and similar competitive examinations, Puzzle questions rarely give just one clue. They typically combine three or more constraints – seating position, facing direction, floor level, schedule day, age relationship, or rank – and require the candidate to place each element systematically, one constraint at a time, rather than guessing the final arrangement. This lesson’s questions are built to that standard.',
  coreConceptsTitle: '3.2 Core Concepts',
  coreConceptsIntro:
    'Puzzles test the ability to organise multiple pieces of information into a single consistent arrangement. In competitive examinations, learners should be proficient in:',
  coreConcepts: [
    'Circular and square seating arrangements, including “immediate right/left,” “second to the right/left,” and “opposite” positional clues.',
    'Alternating-gender or alternating-category seating arrangements.',
    'Floor/building puzzles, where “above,” “below,” and “immediately above/below” clues fix each person’s floor.',
    'Scheduling puzzles involving days of the week or months of the year, including “postponed by,” “after,” and “every nth month” clues.',
    'Age-comparison puzzles involving relative clues (“older than,” “younger than”) and equation-based clues (multiples, sums after a number of years).',
    'Ranking and comparison puzzles, where relative clues (“scored more/less than”) must be chained into a single order.',
    'Distribution puzzles, where a total quantity is split according to a stated pattern (equal increments, ratios, or halving).'
  ],
  commonMistakesTitle: '3.3 Common Mistakes',
  commonMistakes: [
    'In circular seating with everyone facing the centre, confusing the directions: immediate right is the anticlockwise neighbour, and immediate left is the clockwise neighbour.',
    'In “opposite” seating clues, forgetting that with 6 people around a circle, “opposite” means 3 seats away, not simply “not adjacent.”',
    'In floor puzzles, confusing “immediately above” (exactly one floor above) with “above” (anywhere higher, not necessarily adjacent).',
    'In scheduling puzzles, mixing up the two counting methods: for ordinal questions (“the 4th day starting from Monday”), the starting day is Day 1; for “n days after” or “postponed by n days,” counting begins from the following day.',
    'In ranking puzzles, only using the clues that are stated directly, and failing to chain indirect relationships (e.g., A>B and B>C implies A>C) into the full order.',
    'In distribution puzzles, forgetting to add all the shares together and set the sum equal to the given total before solving.'
  ],
  examTipsTitle: '3.4 Examination Tips',
  examTips: [
    'Fix the most specific or absolute clue first (e.g., “X is at the extreme right,” “Y lives on floor 5,” “Z is opposite A”), then place the remaining elements relative to it.',
    'For circular seating, sketch the circle and number the seats (1 to n, clockwise). For people facing the centre, right = anticlockwise and left = clockwise; for people facing outward, the directions are reversed.',
    'For floor puzzles, sketch a simple vertical list from bottom to top rather than tracking floors mentally.',
    'For ordinal questions such as “the 4th day starting from Monday,” count the starting day as Day 1. For “n days after” or “postponed by n days,” begin counting from the following day.',
    'For ranking and comparison puzzles, chain all the given relative clues into a single ordered list before answering.',
    'For distribution puzzles, express every share in terms of one variable, sum them, and set the sum equal to the given total.'
  ]
};

export const PUZZLES_PDF_TA: LessonPdfData = {
  lessonTitle: '8. புதிர்கள் (Puzzles)',
  objectivesTitle: '1. கற்றல் நோக்கங்கள்',
  objectivesPreamble: 'இப்பாடத்தை நிறைவு செய்த பின் கற்போர் பின்வருவனவற்றைச் செய்ய இயலும்:',
  objectives: [
    'பல இட நிபந்தனைகள் கொண்ட வட்ட மற்றும் சதுர இருக்கை அமைப்புப் புதிர்களைத் தீர்த்தல்.',
    'தளம்/கட்டடம், கால அட்டவணை (நாள் மற்றும் மாதம்), பகிர்வுப் புதிர்களை முறையாகத் தீர்த்தல்.',
    'பல சார்புக் குறிப்புகள் கொண்ட வயது ஒப்பீடு மற்றும் தரவரிசைப் புதிர்களைத் தீர்த்தல்.',
    'உத்தித் திட்டமிடல், கவனக் கட்டுப்பாடு, உதவி நாடுதல், சுய மதிப்பீடு மற்றும் சிந்தனை ஆகியவற்றைப் பயன்படுத்தி, போட்டித் தேர்வுத் தரத்திலான பல படிநிலைப் புதிர் வினாக்களைத் திறம்படத் தீர்த்தல்.'
  ],
  overviewTitle: '2. பாடக் கண்ணோட்டம்',
  overview:
    'புதிர்கள் என்பது TNPSC குரூப் 1 மற்றும் அது சார்ந்த போட்டித் தேர்வுகளில் ஒரு முக்கியச் சிக்கல் தீர்க்கும் திறன் தலைப்பாகும். சிக்கலான சூழல்களைப் பகுப்பாய்தல், பல கூறுகளுக்கிடையிலான தொடர்புகளைக் கண்டறிதல், தீர்வு உத்தியை வகுத்தல், முறையான காரணவியல் மூலம் தருக்க முடிவுகளை அடைதல் ஆகிய தேர்வரின் திறன்களை இது சோதிக்கிறது. இப்பாடம் ஒற்றைக் குறிப்பு நினைவுகூர்தலுக்குப் பதிலாக, உயர்நிலை, பல நிபந்தனைச் சிக்கல் தீர்த்தலுக்கு – மாறி மாறி அமரும் ஆண்/பெண் வட்ட இருக்கை அமைப்பு, பல தளக் கட்டடங்கள், நாட்கள் மற்றும் மாதங்களுக்கான கால அட்டவணை, பகிர்வு மற்றும் தரவரிசைப் புதிர்கள் – முக்கியத்துவம் அளிக்கிறது.',
  conceptTitle: '3. கருத்து விளக்கம்',
  examInsightTitle: '3.1 தேர்வு நோக்கு',
  examInsight:
    'TNPSC குரூப் 1 மற்றும் இதுபோன்ற போட்டித் தேர்வுகளில், புதிர் வினாக்கள் ஒரே ஒரு குறிப்பை மட்டும் தருவது அரிது. அவை பொதுவாக மூன்று அல்லது அதற்கு மேற்பட்ட நிபந்தனைகளை – இருக்கை நிலை, நோக்கும் திசை, தள நிலை, அட்டவணை நாள், வயதுத் தொடர்பு, அல்லது தரவரிசை – இணைக்கின்றன; இறுதி அமைப்பை ஊகிக்காமல், ஒவ்வொரு கூறையும் ஒவ்வொரு நிபந்தனையாக முறையாக அமர்த்த வேண்டியுள்ளது. இப்பாடத்தின் வினாக்கள் அந்த தரத்தில் அமைக்கப்பட்டுள்ளன.',
  coreConceptsTitle: '3.2 அடிப்படைக் கருத்துகள்',
  coreConceptsIntro:
    'பல தகவல் துண்டுகளை ஒரே சீரான அமைப்பாக ஒழுங்கமைக்கும் திறனைப் புதிர்கள் சோதிக்கின்றன. போட்டித் தேர்வுகளில் கற்போர் பின்வருவனவற்றில் தேர்ச்சி பெற்றிருக்க வேண்டும்:',
  coreConcepts: [
    '“உடனடி வலம்/இடம்,” “வலமிருந்து/இடமிருந்து இரண்டாவது,” “எதிரே” போன்ற இடக் குறிப்புகள் உள்ளிட்ட வட்ட மற்றும் சதுர இருக்கை அமைப்புகள்.',
    'ஆண்/பெண் அல்லது வகைகள் மாறி மாறி அமரும் இருக்கை அமைப்புகள்.',
    '“மேலே,” “கீழே,” “உடனடியாக மேலே/கீழே” போன்ற குறிப்புகள் ஒவ்வொருவரின் தளத்தையும் நிர்ணயிக்கும் தளம்/கட்டடப் புதிர்கள்.',
    '“ஒத்திவைக்கப்பட்டது,” “பின்னர்,” “ஒவ்வொரு n-ஆவது மாதமும்” போன்ற குறிப்புகளுடன், வாரத்தின் நாட்கள் அல்லது ஆண்டின் மாதங்கள் சார்ந்த கால அட்டவணைப் புதிர்கள்.',
    'சார்புக் குறிப்புகள் (“மூத்தவர்,” “இளையவர்”) மற்றும் சமன்பாட்டு அடிப்படையிலான குறிப்புகள் (மடங்குகள், சில ஆண்டுகளுக்குப் பிந்தைய கூடுதல்) கொண்ட வயது ஒப்பீட்டுப் புதிர்கள்.',
    'சார்புக் குறிப்புகளை (“அதிகம்/குறைவு மதிப்பெண் பெற்றார்”) ஒரே வரிசையாக இணைக்க வேண்டிய தரவரிசை மற்றும் ஒப்பீட்டுப் புதிர்கள்.',
    'ஒரு மொத்த அளவு குறிப்பிட்ட அமைப்பின்படி (சம அதிகரிப்புகள், விகிதங்கள், அல்லது பாதியாக்கல்) பிரிக்கப்படும் பகிர்வுப் புதிர்கள்.'
  ],
  commonMistakesTitle: '3.3 பொதுவான தவறுகள்',
  commonMistakes: [
    'அனைவரும் மையத்தை நோக்கி அமரும் வட்ட இருக்கை அமைப்பில், திசைகளைக் குழப்பிக்கொள்ளுதல்: உடனடி வலம் என்பது எதிர்க்கடிகாரத் திசையிலுள்ள அண்டையர்; உடனடி இடம் என்பது கடிகாரத் திசையிலுள்ள அண்டையர்.',
    '“எதிரே” என்ற இருக்கைக் குறிப்புகளில், வட்டத்தில் 6 பேர் இருக்கும்போது “எதிரே” என்பது வெறுமனே “அருகில் இல்லை” அல்ல, 3 இருக்கைகள் தள்ளி என்பதை மறத்தல்.',
    'தளப் புதிர்களில், “உடனடியாக மேலே” (சரியாக ஒரு தளம் மேலே) என்பதையும் “மேலே” (அருகில் இல்லாமலும் எங்கும் உயரத்தில்) என்பதையும் குழப்பிக்கொள்ளுதல்.',
    'கால அட்டவணைப் புதிர்களில், இரண்டு எண்ணும் முறைகளைக் குழப்பிக்கொள்ளுதல்: வரிசை எண் வினாக்களில் (“திங்கள் முதல் 4-ஆம் நாள்”) தொடக்க நாளே 1-ஆம் நாள்; “n நாட்கள் பின்” அல்லது “n நாட்கள் ஒத்திவைப்பு” வினாக்களில் அடுத்த நாளிலிருந்து எண்ணத் தொடங்க வேண்டும்.',
    'தரவரிசைப் புதிர்களில், நேரடியாகக் கூறப்பட்ட குறிப்புகளை மட்டும் பயன்படுத்தி, மறைமுகத் தொடர்புகளை (எ.கா., A>B, B>C எனில் A>C) முழு வரிசையாக இணைக்கத் தவறுதல்.',
    'பகிர்வுப் புதிர்களில், தீர்க்கும் முன் அனைத்துப் பங்குகளையும் கூட்டி அக்கூடுதலைக் கொடுக்கப்பட்ட மொத்தத்துக்குச் சமப்படுத்த மறத்தல்.'
  ],
  examTipsTitle: '3.4 தேர்வுக் குறிப்புகள்',
  examTips: [
    'மிகக் குறிப்பிட்ட அல்லது உறுதியான குறிப்பை (எ.கா., “X வலது ஓரத்தில் உள்ளார்,” “Y 5-ஆம் தளத்தில் வசிக்கிறார்,” “Z, A-க்கு எதிரே உள்ளார்”) முதலில் நிலைநிறுத்தி, பின்னர் மீதமுள்ளவற்றை அதைப் பொறுத்து அமர்த்தவும்.',
    'வட்ட இருக்கை அமைப்புக்கு, வட்டத்தை வரைந்து இருக்கைகளை (1 முதல் n வரை, கடிகாரத் திசையில்) எண்ணிடவும். மையத்தை நோக்கி அமர்ந்திருப்போருக்கு வலம் = எதிர்க்கடிகாரத் திசை, இடம் = கடிகாரத் திசை; வெளிப்புறம் நோக்கி அமர்ந்திருப்போருக்கு இத்திசைகள் தலைகீழாகும்.',
    'தளப் புதிர்களுக்கு, தளங்களை மனத்தில் மட்டும் பின்தொடராமல், கீழிருந்து மேலாக ஓர் எளிய செங்குத்துப் பட்டியலை வரையவும்.',
    '“திங்கள் முதல் 4-ஆம் நாள்” போன்ற வரிசை எண் வினாக்களில், தொடக்க நாளை 1-ஆம் நாளாக எண்ணவும். “n நாட்கள் பின்” அல்லது “n நாட்கள் ஒத்திவைப்பு” வினாக்களில், அடுத்த நாளிலிருந்து எண்ணத் தொடங்கவும்.',
    'தரவரிசை மற்றும் ஒப்பீட்டுப் புதிர்களுக்கு, விடையளிக்கும் முன் கொடுக்கப்பட்ட அனைத்துச் சார்புக் குறிப்புகளையும் ஒரே வரிசைப் பட்டியலாக இணைக்கவும்.',
    'பகிர்வுப் புதிர்களுக்கு, ஒவ்வொரு பங்கையும் ஒரே மாறியின் அடிப்படையில் வெளிப்படுத்தி, அவற்றைக் கூட்டி, கொடுக்கப்பட்ட மொத்தத்துக்குச் சமப்படுத்தவும்.'
  ]
};
