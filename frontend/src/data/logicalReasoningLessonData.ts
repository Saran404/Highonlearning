/** Exact Logical Reasoning Lesson Theory extracted directly from LogicalReasoningenglish and LogicalReasoningtamil PDFs. */
import type { LessonPdfData } from './ratioLessonData';

export const LOGICAL_REASONING_PDF_EN: LessonPdfData = {
  lessonTitle: '5. Logical Reasoning',
  objectivesTitle: '1. Learning Objectives',
  objectivesPreamble: 'The learner will be able to:',
  objectives: [
    'Solve coding-decoding, blood relation, and direction-sense problems using systematic pattern identification.',
    'Evaluate syllogisms (statements and conclusions) using valid logical rules.',
    'Solve analogy, classification, seating arrangement, ranking, and letter-series problems accurately.',
    'Solve multi-step, competitive-examination-standard questions on Logical Reasoning efficiently, using Attention Control, Task Strategies, Self-Monitoring, and Help-Seeking.'
  ],
  overviewTitle: '2. Lesson Overview',
  overview:
    'Logical Reasoning is a core Logical Reasoning Skills topic in TNPSC Group 1 and allied competitive examinations, testing a candidate’s ability to analyse information, identify logical relationships, evaluate arguments, and draw valid conclusions systematically. This lesson emphasises higher-order, multi-step problem solving – multi-generation blood relations, direction problems requiring the Pythagorean relationship, two-conclusion syllogisms, and multi-condition seating/ranking puzzles – rather than single-step pattern recall.',
  conceptTitle: '3. Concept Explanation',
  examInsightTitle: '3.1 Exam Insight',
  examInsight:
    'In TNPSC Group 1 and similar competitive examinations, Logical Reasoning questions rarely stop at “identify the pattern.” They typically combine two or more conditions – a multi-step family relationship, a series of directional turns, two syllogistic statements with two conclusions, or several seating constraints – and require the candidate to track information systematically before answering. The lesson progresses from foundational questions to multi-step logical reasoning problems.',
  coreConceptsTitle: '3.2 Core Concepts',
  coreConceptsIntro:
    'Logical Reasoning tests the ability to identify relationships and apply systematic rules rather than compute numbers. In competitive examinations, learners should be proficient in:',
  coreConcepts: [
    'Coding-decoding: identifying the letter-shift or substitution pattern from a given example, then applying it to a new word.',
    'Blood relations: tracing family relationships across generations, paying close attention to gender and generation cues (“only son,” “only daughter,” “father’s father”).',
    'Direction sense: tracking cumulative displacement after a series of moves and turns, using the Pythagorean relationship when the net displacement is not a straight line.',
    'Syllogisms: applying valid rules (All A are B + All B are C → All A are C; Some A are B + All B are C → Some A are C) and recognising invalid conclusions (No A are B + All B are C does NOT give No A are C).',
    'Analogies: identifying the relationship type (function, category, part-whole, degree) between the first pair before applying it to the second.',
    'Classification: identifying the shared category among most items to isolate the one that does not belong.',
    'Letter/alphabet series: identifying the pattern of skips or shifts between consecutive terms.',
    'Seating arrangement and ranking: systematically placing each element using the given constraints, one at a time, and computing rank-from-top/rank-from-bottom relationships.'
  ],
  commonMistakesTitle: '3.3 Common Mistakes',
  commonMistakes: [
    'In blood relation problems, misreading “only son” or “only daughter” as “only child.” “Only son” means there are no other sons (there may still be daughters), and “only daughter” means there are no other daughters (there may still be sons).',
    'In direction problems, forgetting that opposite-direction movements cancel out before computing net displacement.',
    'In syllogisms, assuming a “No A are B” premise combined with “All B are C” gives “No A are C” – this is a common invalid conclusion.',
    'In ranking problems, using rank-from-top + rank-from-bottom directly as the total, instead of subtracting 1 (since the person is counted twice).',
    'In seating arrangement problems, placing elements based on assumed positions instead of strictly following the given constraints one at a time.',
    'In coding-decoding, assuming the same shift applies to every letter without verifying it against the given example first.'
  ],
  examTipsTitle: '3.4 Examination Tips',
  examTips: [
    'For blood relations, draw a quick family tree or use short-form notation as you read each clue – do not try to hold multi-generation relationships in your head.',
    'For direction problems with a right-angle net displacement, apply the Pythagorean relationship (distance = √(x²+y²)) directly.',
    'For syllogisms, test each conclusion against the valid syllogism rules rather than relying on intuition – “Some” and “All” statements behave differently when combined.',
    'For ranking, always use: Total = (rank from top) + (rank from bottom) − 1.',
    'For seating arrangement and stacking puzzles, place the most specific constraint (e.g., “at the extreme right,” “at the bottom”) first, then work outward from it.'
  ]
};

export const LOGICAL_REASONING_PDF_TA: LessonPdfData = {
  lessonTitle: '5. தருக்கக் காரணவியல் (Logical Reasoning)',
  objectivesTitle: '1. கற்றல் நோக்கங்கள்',
  objectivesPreamble: 'இப்பாடத்தை நிறைவு செய்த பின் கற்போர் பின்வருவனவற்றைச் செய்ய இயலும்:',
  objectives: [
    'முறையான அமைப்பு அடையாளத்தைப் பயன்படுத்தி, குறியீடு–குறிவிலக்கம், இரத்த உறவுகள், திசை அறிதல் ஆகிய கணக்குகளைத் தீர்த்தல்.',
    'செல்லத்தக்க தருக்க விதிகளைப் பயன்படுத்தி, தருக்க முடிவுகளை (கூற்றுகள் மற்றும் முடிவுகள்) மதிப்பிடுதல்.',
    'ஒப்புமை, வகைப்படுத்தல், இருக்கை அமைப்பு, தரவரிசை, எழுத்துத் தொடர் ஆகிய கணக்குகளைத் துல்லியமாகத் தீர்த்தல்.',
    'கவனக் கட்டுப்பாடு, பணி உத்திகள், சுயக் கண்காணிப்பு, உதவி நாடுதல் ஆகியவற்றைப் பயன்படுத்தி, போட்டித் தேர்வுத் தரத்திலான பல படிநிலைத் தருக்கக் காரணவியல் வினாக்களைத் திறம்படத் தீர்த்தல்.'
  ],
  overviewTitle: '2. பாடக் கண்ணோட்டம்',
  overview:
    'தருக்கக் காரணவியல் என்பது TNPSC குரூப் 1 மற்றும் அது சார்ந்த போட்டித் தேர்வுகளில் ஒரு முக்கியத் தருக்கத் திறன் தலைப்பாகும். தகவல்களைப் பகுப்பாய்தல், தருக்கத் தொடர்புகளை அடையாளம் காணுதல், வாதங்களை மதிப்பிடுதல், செல்லத்தக்க முடிவுகளை முறையாகப் பெறுதல் ஆகிய தேர்வரின் திறன்களை இது சோதிக்கிறது. இப்பாடம் ஒருபடி அமைப்பு நினைவுகூர்தலுக்குப் பதிலாக, உயர்நிலை, பல படிநிலைச் சிக்கல் தீர்த்தலுக்கு – பல தலைமுறை இரத்த உறவுகள், பிதாகரஸ் தொடர்பு தேவைப்படும் திசைக் கணக்குகள், இரு முடிவுகள் கொண்ட தருக்க வினாக்கள், பல நிபந்தனை இருக்கை/தரவரிசைப் புதிர்கள் – முக்கியத்துவம் அளிக்கிறது.',
  conceptTitle: '3. கருத்து விளக்கம்',
  examInsightTitle: '3.1 தேர்வு நோக்கு',
  examInsight:
    'TNPSC குரூப் 1 மற்றும் இதுபோன்ற போட்டித் தேர்வுகளில், தருக்கக் காரணவியல் வினாக்கள் “அமைப்பைக் கண்டறிக” என்பதோடு நிற்பது அரிது. அவை பொதுவாக இரண்டு அல்லது அதற்கு மேற்பட்ட நிபந்தனைகளை – பல படிநிலைக் குடும்ப உறவு, தொடர்ச்சியான திசைத் திருப்பங்கள், இரு முடிவுகளுடன் கூடிய இரண்டு தருக்கக் கூற்றுகள், அல்லது பல இருக்கை நிபந்தனைகள் – இணைக்கின்றன; விடையளிக்கும் முன் தேர்வர் தகவல்களை முறையாகப் பின்தொடர வேண்டியுள்ளது. இப்பாடம் அடிப்படை வினாக்களிலிருந்து பல படிநிலைத் தருக்கக் காரணவியல் கணக்குகளை நோக்கிப் படிப்படியாக முன்னேறுகிறது.',
  coreConceptsTitle: '3.2 அடிப்படைக் கருத்துகள்',
  coreConceptsIntro:
    'தருக்கக் காரணவியல், எண்களைக் கணக்கிடுவதைவிட, தொடர்புகளை அடையாளம் கண்டு முறையான விதிகளைப் பயன்படுத்தும் திறனைச் சோதிக்கிறது. போட்டித் தேர்வுகளில் கற்போர் பின்வருவனவற்றில் தேர்ச்சி பெற்றிருக்க வேண்டும்:',
  coreConcepts: [
    'குறியீடு–குறிவிலக்கம்: கொடுக்கப்பட்ட எடுத்துக்காட்டிலிருந்து எழுத்து நகர்வு அல்லது பதிலீட்டு அமைப்பைக் கண்டறிந்து, அதைப் புதிய சொல்லுக்குப் பயன்படுத்துதல்.',
    'இரத்த உறவுகள்: பாலினம் மற்றும் தலைமுறைக் குறிப்புகளில் (“ஒரே மகன்,” “ஒரே மகள்,” “தந்தையின் தந்தை”) கவனம் செலுத்தி, தலைமுறைகளுக்கிடையிலான குடும்ப உறவுகளைப் பின்தொடர்தல்.',
    'திசை அறிதல்: தொடர்ச்சியான நகர்வுகள் மற்றும் திருப்பங்களுக்குப் பின் ஏற்படும் மொத்த இடப்பெயர்ச்சியைக் கண்காணித்தல்; நிகர இடப்பெயர்ச்சி நேர்கோட்டில் இல்லாதபோது பிதாகரஸ் தொடர்பைப் பயன்படுத்துதல்.',
    'தருக்க முடிவுகள்: செல்லத்தக்க விதிகளைப் பயன்படுத்துதல் (எல்லா A-யும் B + எல்லா B-யும் C → எல்லா A-யும் C; சில A, B + எல்லா B-யும் C → சில A, C) மற்றும் செல்லாத முடிவுகளை அடையாளம் காணுதல் (எந்த A-யும் B அல்ல + எல்லா B-யும் C என்பது “எந்த A-யும் C அல்ல” என்ற முடிவைத் தராது).',
    'ஒப்புமைகள்: முதல் இணையின் தொடர்பு வகையை (பயன்பாடு, வகைமை, பகுதி–முழுமை, அளவு) கண்டறிந்து, பின்னர் அதை இரண்டாம் இணைக்குப் பயன்படுத்துதல்.',
    'வகைப்படுத்தல்: பெரும்பாலான உருப்படிகளுக்குப் பொதுவான வகையைக் கண்டறிந்து, பொருந்தாத ஒன்றை தனிப்படுத்துதல்.',
    'எழுத்து/அகரவரிசைத் தொடர்: அடுத்தடுத்த உறுப்புகளுக்கிடையிலான தாவல் அல்லது நகர்வு அமைப்பைக் கண்டறிதல்.',
    'இருக்கை அமைப்பு மற்றும் தரவரிசை: கொடுக்கப்பட்ட நிபந்தனைகளை ஒவ்வொன்றாகப் பயன்படுத்தி ஒவ்வொருவரையும் முறையாக அமர்த்துதல்; மேலிருந்து/கீழிருந்து தரவரிசைத் தொடர்புகளைக் கணக்கிடுதல்.'
  ],
  commonMistakesTitle: '3.3 பொதுவான தவறுகள்',
  commonMistakes: [
    'இரத்த உறவுக் கணக்குகளில், “ஒரே மகன்” அல்லது “ஒரே மகள்” என்பதை “ஒரே பிள்ளை” எனத் தவறாகப் புரிந்துகொள்ளுதல். “ஒரே மகன்” என்றால் வேறு மகன்கள் இல்லை (மகள்கள் இருக்கலாம்); “ஒரே மகள்” என்றால் வேறு மகள்கள் இல்லை (மகன்கள் இருக்கலாம்).',
    'திசைக் கணக்குகளில், நிகர இடப்பெயர்ச்சியைக் கணக்கிடும் முன் எதிர்த்திசை நகர்வுகள் ஒன்றையொன்று நீக்குகின்றன என்பதை மறத்தல்.',
    'தருக்க முடிவுகளில், “எந்த A-யும் B அல்ல” என்ற கூற்றும் “எல்லா B-யும் C” என்ற கூற்றும் சேர்ந்து “எந்த A-யும் C அல்ல” எனத் தரும் என்று கருதுதல் – இது பொதுவான செல்லாத முடிவாகும்.',
    'தரவரிசைக் கணக்குகளில், 1-ஐக் கழிக்காமல் (அந்நபர் இருமுறை எண்ணப்படுவதால்) மேலிருந்து தரவரிசை + கீழிருந்து தரவரிசை என்பதையே மொத்தமாகக் கொள்ளுதல்.',
    'இருக்கை அமைப்புக் கணக்குகளில், கொடுக்கப்பட்ட நிபந்தனைகளை ஒவ்வொன்றாகக் கண்டிப்பாகப் பின்பற்றாமல், ஊகித்த இடங்களின் அடிப்படையில் அமர்த்துதல்.',
    'குறியீடு–குறிவிலக்கத்தில், கொடுக்கப்பட்ட எடுத்துக்காட்டுடன் முதலில் சரிபார்க்காமல், ஒவ்வொரு எழுத்துக்கும் ஒரே நகர்வு பொருந்தும் எனக் கருதுதல்.'
  ],
  examTipsTitle: '3.4 தேர்வுக் குறிப்புகள்',
  examTips: [
    'இரத்த உறவுகளுக்கு, ஒவ்வொரு குறிப்பையும் படிக்கும்போதே ஒரு விரைவான குடும்ப மரத்தை வரையவும் அல்லது சுருக்கக் குறியீடுகளைப் பயன்படுத்தவும் – பல தலைமுறை உறவுகளை மனத்தில் மட்டும் வைக்க முயல வேண்டாம்.',
    'நிகர இடப்பெயர்ச்சி செங்கோணம் அமைக்கும் திசைக் கணக்குகளுக்கு, பிதாகரஸ் தொடர்பை (தூரம் = √(x²+y²)) நேரடியாகப் பயன்படுத்தவும்.',
    'தருக்க முடிவுகளுக்கு, உள்ளுணர்வை நம்பாமல், ஒவ்வொரு முடிவையும் செல்லத்தக்க விதிகளுடன் சோதிக்கவும் – “சில” மற்றும் “எல்லா” கூற்றுகள் இணையும்போது வெவ்வேறு விதமாகச் செயல்படுகின்றன.',
    'தரவரிசைக்கு எப்போதும் பயன்படுத்தவும்: மொத்தம் = (மேலிருந்து தரவரிசை) + (கீழிருந்து தரவரிசை) − 1.',
    'இருக்கை அமைப்பு மற்றும் அடுக்குப் புதிர்களில், மிகக் குறிப்பிட்ட நிபந்தனையை (எ.கா., “வலது ஓரத்தில்,” “அடியில்”) முதலில் அமர்த்தி, பின்னர் அதிலிருந்து விரிவுபடுத்தவும்.'
  ]
};
