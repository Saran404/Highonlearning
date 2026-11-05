# -*- coding: utf-8 -*-
"""Generates 08_logical_reasoning_bilingual_seed.sql containing all 85 questions from English and Tamil Logical Reasoning PDFs."""
import json
import os

def escape_sql(text: str) -> str:
    if text is None:
        return 'NULL'
    return "N'" + text.replace("'", "''") + "'"

def main():
    # 25 Worked Examples (English)
    worked_en = [
        # Q1
        ("If CAT is coded as DBU, code DOG using the same pattern.",
         ["EQH", "EPI", "EPH", "FPI"], 2,
         "Each letter shifts forward by 1: D→E, O→P, G→H. Key Learning Point: In coding-decoding, first verify the shift pattern using the given example, then apply the same shift to each letter of the new word.", "EASY"),
        # Q2
        ("Pointing to a photo, a man says, “She is the daughter of my mother’s only son.” How is she related to him?",
         ["Sister", "Daughter", "Niece", "Wife"], 1,
         "Mother’s only son = the man himself. Daughter of himself = his daughter. Key Learning Point: “Only son/daughter” phrases often refer back to the speaker – check this possibility before assuming a different family member.", "EASY"),
        # Q3
        ("A man walks 5 km North, then turns right and walks 5 km. Which direction is he now facing?",
         ["North", "South", "East", "West"], 2,
         "Facing North, a right turn faces him East. Key Learning Point: A right turn from North faces East; a right turn from East faces South, and so on, clockwise.", "EASY"),
        # Q4
        ("Doctor : Hospital :: Teacher : ?",
         ["Student", "School", "Book", "Class"], 1,
         "A doctor works at a hospital; a teacher works at a school. Key Learning Point: Identify the relationship type (here, “workplace of”) in the first pair before applying it to the second.", "EASY"),
        # Q5
        ("Find the odd one out: Apple, Banana, Carrot, Mango.",
         ["Apple", "Banana", "Carrot", "Mango"], 2,
         "Apple, Banana, and Mango are fruits; Carrot is a vegetable. Key Learning Point: Identify the shared category among most items first, then isolate the one that does not fit.", "EASY"),
        # Q6
        ("In a code, MOUSE is written as NPVTF. What is the code for RABBIT using the same pattern?",
         ["SBCCJU", "SBCDJU", "SCCCJU", "SBDCJU"], 0,
         "Verify pattern: M→N, O→P, U→V, S→T, E→F – each letter shifts forward by 1. RABBIT: R→S, A→B, B→C, B→C, I→J, T→U = SBCCJU. Key Learning Point: Always verify the shift using every letter of the given example before applying it, since a single-letter check can be misleading.", "EASY"),
        # Q7
        ("Introducing a man, a woman said, “He is the son of the only daughter of my father.” How is the woman related to the man?",
         ["Mother", "Sister", "Aunt", "Grandmother"], 0,
         "Only daughter of her father = the woman herself. Son of herself = her son. Key Learning Point: Trace the relationship one step at a time, resolving each “only son/daughter” reference before moving to the next.", "EASY"),
        # Q8
        ("A is B’s brother. C is D’s mother. A’s son is D’s brother. What is the relation between B and D?",
         ["Uncle", "Father", "Brother", "Cousin"], 0,
         "A’s son is D’s brother → D is also A’s child → A is D’s father. B is A’s brother → B is D’s uncle. Key Learning Point: Draw a quick family tree for multi-clue blood relation problems rather than tracking relationships mentally.", "MEDIUM"),
        # Q9
        ("A man walks 3 km East, then 4 km North, then 3 km West. How far is he from the starting point, and in which direction?",
         ["3 km North", "4 km North", "5 km North", "7 km North"], 1,
         "East and West movements cancel out (3 km each), leaving only the 4 km North displacement. Key Learning Point: Opposite-direction movements cancel before computing net displacement.", "EASY"),
        # Q10
        ("A man walks 6 km North then 8 km East. How far is he from the starting point?",
         ["8 km", "10 km", "12 km", "14 km"], 1,
         "Distance = √(6²+8²) = √(36+64) = √100 = 10 km. Key Learning Point: When the net displacement forms a right angle, apply the Pythagorean relationship.", "EASY"),
        # Q11
        ("Statements: All cats are animals. All animals are living things. Conclusion: All cats are living things. Does the conclusion follow?",
         ["Conclusion follows", "Conclusion does not follow", "Cannot be determined", "Both conclusions follow"], 0,
         "All A are B, and all B are C, therefore all A are C – a valid chain syllogism. Key Learning Point: “All A are B” combined with “All B are C” always validly gives “All A are C.”", "EASY"),
        # Q12
        ("Statements: Some pens are books. All books are papers. Conclusions: I. Some pens are papers. II. All papers are books. Which conclusion(s) follow?",
         ["Only I follows", "Only II follows", "Both I and II follow", "Neither I nor II follows"], 0,
         "I follows: some pens are books, and all books are papers, so some pens are papers. II does not follow: “all books are papers” cannot be reversed to “all papers are books.” Key Learning Point: A universal statement (“All B are C”) cannot be reversed into “All C are B” – check each conclusion independently.", "MEDIUM"),
        # Q13
        ("Page : Book :: Petal : ?",
         ["Root", "Stem", "Flower", "Seed"], 2,
         "A page is a part of a book; a petal is a part of a flower. Key Learning Point: In part-whole analogies, choose the whole to which the part directly and only belongs; avoid options where the part could belong to more than one whole.", "EASY"),
        # Q14
        ("Find the odd one out: Triangle, Square, Circle, Cube.",
         ["Triangle", "Square", "Circle", "Cube"], 3,
         "Triangle, Square, and Circle are 2D shapes; Cube is a 3D solid. Key Learning Point: Look for a category difference (here, dimensionality) rather than a surface similarity.", "EASY"),
        # Q15
        ("Find the next term: B, D, G, K, P, ?",
         ["T", "U", "V", "W"], 2,
         "The gap increases by 1 each time: +2, +3, +4, +5, +6. P+6 = V. Key Learning Point: When the gap between terms itself increases steadily, identify the gap pattern before finding the next term.", "EASY"),
        # Q16
        ("Find the missing term: AZ, BY, CX, DW, ?",
         ["EV", "EU", "EW", "FV"], 0,
         "First letter moves forward (A,B,C,D,E); second letter moves backward (Z,Y,X,W,V). Key Learning Point: In two-letter series, check whether each position follows its own independent pattern.", "EASY"),
        # Q17
        ("Five friends A, B, C, D, E sit in a row. B is immediately right of A. C is immediately left of D. E is between B and C. If A sits at one end, who sits at the other end?",
         ["B", "C", "D", "E"], 2,
         "Order: A, B, E, C, D. Answer: D. Key Learning Point: Place the most specific constraint (here, “A at one end”) first, then build outward using the remaining clues.", "MEDIUM"),
        # Q18
        ("In a class of 40 students, Raj ranks 12th from the top. What is his rank from the bottom?",
         ["27", "28", "29", "30"], 2,
         "Rank from bottom = Total − rank from top + 1 = 40 − 12 + 1 = 29. Key Learning Point: Rank from bottom = Total students − rank from top + 1.", "EASY"),
        # Q19
        ("In a row of 30 students, Meena is 15th from the left and Priya is 10th from the right. How many students are between them?",
         ["4", "5", "6", "7"], 1,
         "Priya’s position from left = 30 − 10 + 1 = 21. Students between positions 15 and 21 = 21 − 15 − 1 = 5. Key Learning Point: Convert all positions to the same reference direction (left or right) before comparing them.", "MEDIUM"),
        # Q20
        ("If FRIEND is written as HTKGPF, how is CANDLE written in the same code?",
         ["ECPFNG", "ECPFMG", "EDPFNG", "ECQFNG"], 0,
         "Verify pattern: each letter shifts forward by 2 (F→H, R→T, I→K, E→G, N→P, D→F). CANDLE: C→E, A→C, N→P, D→F, L→N, E→G = ECPFNG. Key Learning Point: Confirm the shift value using multiple letters of the given example before applying it to a new word.", "EASY"),
        # Q21
        ("Pointing to a man, a woman says, “His mother is the only daughter of my mother.” How is the woman related to the man?",
         ["Mother", "Sister", "Grandmother", "Aunt"], 0,
         "Only daughter of her mother = the woman herself. So “his mother” = the woman → she is his mother. Key Learning Point: When a clue defines someone as “the only daughter/son of my parent,” check first whether it refers to the speaker.", "EASY"),
        # Q22
        ("A man starts walking facing North. He turns 90° clockwise, then 180°, then 90° anticlockwise. Which direction is he facing now?",
         ["North", "South", "East", "West"], 1,
         "North → (90° CW) → East → (180°) → West → (90° ACW) → South. Key Learning Point: Track each turn step by step on a mental compass rather than trying to compute the total angle at once.", "EASY"),
        # Q23
        ("Statements: No teachers are students. All students are learners. Conclusion: No teachers are learners. Does the conclusion follow?",
         ["Conclusion follows", "Conclusion does not follow", "Cannot be determined", "Both conclusions follow"], 1,
         "“No A are B” combined with “All B are C” does not validly give “No A are C” – teachers could still be learners through another route. Key Learning Point: A negative premise (“No A are B”) combined with a positive premise (“All B are C”) never validly produces a negative conclusion about A and C.", "MEDIUM"),
        # Q24
        ("5 : 25 :: 7 : ?",
         ["35", "42", "49", "56"], 2,
         "The relationship is “square of the number”: 5²=25, so 7²=49. Key Learning Point: Numeric analogies often use a mathematical relationship (square, cube, double) – verify it against the first pair before applying it.", "EASY"),
        # Q25
        ("Five boxes P, Q, R, S, T are stacked. P is directly above Q. Q is directly above R. S is directly above T. T is at the bottom. Find the order from top to bottom.",
         ["P, Q, R, S, T", "Q, P, R, S, T", "P, Q, S, R, T", "P, R, Q, S, T"], 0,
         "T is at the bottom (position 5). S is directly above T (position 4). P, Q, R fill positions 1, 2, 3 in that order since P is above Q is above R. Key Learning Point: Place the fixed reference point (“T at the bottom”) first, then build the rest of the stack around it.", "MEDIUM")
    ]

    # 25 Worked Examples (Tamil)
    worked_ta = [
        # Q1
        ("CAT என்பது DBU எனக் குறியிடப்பட்டால், அதே அமைப்பில் DOG-ஐக் குறியிடுக.",
         ["EQH", "EPI", "EPH", "FPI"], 2,
         "ஒவ்வோர் எழுத்தும் 1 இடம் முன்னோக்கி நகர்கிறது: D→E, O→P, G→H. முக்கியக் கற்றல் கருத்து: குறியீடு–குறிவிலக்கத்தில், முதலில் கொடுக்கப்பட்ட எடுத்துக்காட்டைக் கொண்டு நகர்வு அமைப்பைச் சரிபார்த்து, பின்னர் அதே நகர்வைப் புதிய சொல்லின் ஒவ்வோர் எழுத்துக்கும் பயன்படுத்தவும்."),
        # Q2
        ("ஒரு புகைப்படத்தைச் சுட்டிக்காட்டி ஒருவர், “இவள் என் தாயின் ஒரே மகனின் மகள்” என்கிறார். அவள் அவருக்கு என்ன உறவு?",
         ["சகோதரி", "மகள்", "மருமகள் (உடன்பிறந்தவரின் மகள்)", "மனைவி"], 1,
         "தாயின் ஒரே மகன் = அவரே. அவருடைய மகள் = அவரது மகள். முக்கியக் கற்றல் கருத்து: “ஒரே மகன்/மகள்” என்ற சொற்றொடர்கள் பெரும்பாலும் பேசுபவரையே குறிக்கின்றன – வேறு குடும்ப உறுப்பினரைக் கருதும் முன் இச்சாத்தியத்தைச் சரிபார்க்கவும்."),
        # Q3
        ("ஒருவர் 5 கி.மீ வடக்கே நடந்து, பின்னர் வலப்புறம் திரும்பி 5 கி.மீ நடக்கிறார். அவர் இப்போது எத்திசையை நோக்கியுள்ளார்?",
         ["வடக்கு", "தெற்கு", "கிழக்கு", "மேற்கு"], 2,
         "வடக்கை நோக்கியிருக்கும்போது வலப்புறம் திரும்பினால் கிழக்கை நோக்குவார். முக்கியக் கற்றல் கருத்து: வடக்கிலிருந்து வலப்புறத் திருப்பம் கிழக்கை நோக்கும்; கிழக்கிலிருந்து வலப்புறத் திருப்பம் தெற்கை நோக்கும் – இவ்வாறு கடிகாரச் சுற்றில் தொடரும்."),
        # Q4
        ("மருத்துவர் : மருத்துவமனை :: ஆசிரியர் : ?",
         ["மாணவர்", "பள்ளி", "புத்தகம்", "வகுப்பு"], 1,
         "மருத்துவர் மருத்துவமனையில் பணிபுரிகிறார்; ஆசிரியர் பள்ளியில் பணிபுரிகிறார். முக்கியக் கற்றல் கருத்து: இரண்டாம் இணைக்குப் பயன்படுத்தும் முன், முதல் இணையின் தொடர்பு வகையை (இங்கு, “பணியிடம்”) கண்டறியவும்."),
        # Q5
        ("பொருந்தாததைக் கண்டறிக: ஆப்பிள், வாழைப்பழம், கேரட், மாம்பழம்.",
         ["ஆப்பிள்", "வாழைப்பழம்", "கேரட்", "மாம்பழம்"], 2,
         "ஆப்பிள், வாழைப்பழம், மாம்பழம் ஆகியவை பழங்கள்; கேரட் ஒரு காய்கறி. முக்கியக் கற்றல் கருத்து: முதலில் பெரும்பாலான உருப்படிகளுக்குப் பொதுவான வகையைக் கண்டறிந்து, பின்னர் பொருந்தாதhost ஒன்றை தனிப்படுத்தவும்."),
        # Q6
        ("ஒரு குறியீட்டில் MOUSE என்பது NPVTF என எழுதப்படுகிறது. அதே அமைப்பில் RABBIT-க்கான குறியீடு என்ன?",
         ["SBCCJU", "SBCDJU", "SCCCJU", "SBDCJU"], 0,
         "அமைப்பைச் சரிபார்க்க: M→N, O→P, U→V, S→T, E→F – ஒவ்வோர் எழுத்தும் 1 இடம் முன்னோக்கி நகர்கிறது. RABBIT: R→S, A→B, B→C, B→C, I→J, T→U = SBCCJU. முக்கியக் கற்றல் கருத்து: ஓர் எழுத்தை மட்டும் சரிபார்ப்பது தவறாக வழிநடத்தக்கூடும் என்பதால், பயன்படுத்தும் முன் கொடுக்கப்பட்ட எடுத்துக்காட்டின் ஒவ்வோர் எழுத்தையும் கொண்டு நகர்வைச் சரிபார்க்கவும்."),
        # Q7
        ("ஒருவரை அறிமுகப்படுத்தும்போது ஒரு பெண், “இவர் என் தந்தையின் ஒரே மகளின் மகன்” என்கிறார். அப்பெண் அவருக்கு என்ன உறவு?",
         ["தாய்", "சகோதரி", "அத்தை", "பாட்டி"], 0,
         "அவரது தந்தையின் ஒரே மகள் = அப்பெண்ணே. அவரது மகன் = அவருடைய மகன். முக்கியக் கற்றல் கருத்து: ஒவ்வொரு “ஒரே மகன்/மகள்” குறிப்பையும் தீர்த்த பின்னரே அடுத்ததற்குச் சென்று, உறவை ஒவ்வொரு படியாகப் பின்தொடரவும்."),
        # Q8
        ("A என்பவர் B-இன் சகோதரர். C என்பவர் D-இன் தாய். A-இன் மகன் D-இன் சகோதரர். B-க்கும் D-க்கும் இடையிலான உறவு என்ன?",
         ["தந்தையின் சகோதரர்", "தந்தை", "சகோதரர்", "ஒன்றுவிட்ட உடன்பிறப்பு (Cousin)"], 0,
         "A-இன் மகன் D-இன் சகோதரர் → D-யும் A-இன் பிள்ளை → A என்பவர் D-இன் தந்தை. B என்பவர் A-இன் சகோதரர் → B என்பவர் D-இன் தந்தையின் சகோதரர் (Uncle). முக்கியக் கற்றல் கருத்து: பல குறிப்புகள் கொண்ட இரத்த உறவுக் கணக்குகளில், உறவுகளை மனத்தில் மட்டும் பின்தொடராமல் விரைவான குடும்ப மரம் வரையவும்."),
        # Q9
        ("ஒருவர் 3 கி.மீ கிழக்கே, பின்னர் 4 கி.மீ வடக்கே, பின்னர் 3 கி.மீ மேற்கே நடக்கிறார். அவர் தொடக்கப் புள்ளியிலிருந்து எவ்வளவு தூரத்தில், எத்திசையில் உள்ளார்?",
         ["3 கி.மீ வடக்கு", "4 கி.மீ வடக்கு", "5 கி.மீ வடக்கு", "7 கி.மீ வடக்கு"], 1,
         "கிழக்கு மற்றும் மேற்கு நகர்வுகள் (தலா 3 கி.மீ) ஒன்றையொன்று நீக்குகின்றன; 4 கி.மீ வடக்கு இடப்பெயர்ச்சி மட்டுமே மீதமுள்ளது. முக்கியக் கற்றல் கருத்து: நிகர இடப்பெயர்ச்சியைக் கணக்கிடும் முன் எதிர்த்திசை நகர்வுகள் ஒன்றையொன்று நீக்குகின்றன."),
        # Q10
        ("ஒருவர் 6 கி.மீ வடக்கே, பின்னர் 8 கி.மீ கிழக்கே நடக்கிறார். அவர் தொடக்கப் புள்ளியிலிருந்து எவ்வளவு தூரத்தில் உள்ளார்?",
         ["8 கி.மீ", "10 கி.மீ", "12 கி.மீ", "14 கி.மீ"], 1,
         "தூரம் = √(6²+8²) = √(36+64) = √100 = 10 கி.மீ. முக்கியக் கற்றல் கருத்து: நிகர இடப்பெயர்ச்சி செங்கோணம் அமைக்கும்போது, பிதாகரஸ் தொடர்பைப் பயன்படுத்தவும்."),
        # Q11
        ("கூற்றுகள்: எல்லாப் பூனைகளும் விலங்குகள். எல்லா விலங்குகளும் உயிரினங்கள். முடிவு: எல்லாப் பூனைகளும் உயிரினங்கள். முடிவு பொருந்துமா?",
         ["முடிவு பொருந்துகிறது", "முடிவு பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டு முடிவுகளும் பொருந்துகின்றன"], 0,
         "எல்லா A-யும் B, எல்லா B-யும் C, எனவே எல்லா A-யும் C – இது செல்லத்தக்க சங்கிலித் தருக்கம். முக்கியக் கற்றல் கருத்து: “எல்லா A-யும் B” என்பதும் “எல்லா B-யும் C” என்பதும் இணைந்தால், எப்போதும் செல்லத்தக்க வகையில் “எல்லா A-யும் C” கிடைக்கும்."),
        # Q12
        ("கூற்றுகள்: சில பேனாக்கள் புத்தகங்கள். எல்லாப் புத்தகங்களும் காகிதங்கள். முடிவுகள்: I. சில பேனாக்கள் காகிதங்கள். II. எல்லாக் காகிதங்களும் புத்தகங்கள். எந்த முடிவு(கள்) பொருந்தும்?",
         ["I மட்டும் பொருந்துகிறது", "II மட்டும் பொருந்துகிறது", "I, II இரண்டும் பொருந்துகின்றன", "I-உம் II-உம் பொருந்தவில்லை"], 0,
         "I பொருந்துகிறது: சில பேனாக்கள் புத்தகங்கள், எல்லாப் புத்தகங்களும் காகிதங்கள்; எனவே சில பேனாக்கள் காகிதங்கள். II பொருந்தவில்லை: “எல்லாப் புத்தகங்களும் காகிதங்கள்” என்பதை “எல்லாக் காகிதங்களும் புத்தகங்கள்” எனத் திருப்பிக் கூற இயலாது. முக்கியக் கற்றல் கருத்து: ஒரு பொதுக் கூற்றை (“எல்லா B-யும் C”) “எல்லா C-யும் B” எனத் திருப்பிக் கூற இயலாது – ஒவ்வொரு முடிவையும் தனித்தனியாகச் சரிபார்க்கவும்."),
        # Q13
        ("பக்கம் : புத்தகம் :: இதழ் : ?",
         ["வேர்", "தண்டு", "பூ", "விதை"], 2,
         "பக்கம் புத்தகத்தின் ஒரு பகுதி; இதழ் பூவின் ஒரு பகுதி. முக்கியக் கற்றல் கருத்து: பகுதி–முழுமை ஒப்புமைகளில், அப்பகுதி நேரடியாகவும் தனித்தும் சேரும் முழுமையைத் தேர்ந்தெடுக்கவும்; அப்பகுதி ஒன்றுக்கு மேற்பட்ட முழுமைகளுக்குச் சேரக்கூடிய விடைகளைத் தவிர்க்கவும்."),
        # Q14
        ("பொருந்தாததைக் கண்டறிக: முக்கோணம், சதுரம், வட்டம், கனசதுரம்.",
         ["முக்கோணம்", "சதுரம்", "வட்டம்", "கனசதுரம்"], 3,
         "முக்கோணம், சதுரம், வட்டம் ஆகியவை இருபரிமாண வடிவங்கள்; கனசதுரம் ஒரு முப்பரிமாணத் திண்மம். முக்கியக் கற்றல் கருத்து: மேலோட்டமான ஒற்றுமையைவிட, வகைமை வேறுபாட்டை (இங்கு, பரிமாணம்) தேடவும்."),
        # Q15
        ("அடுத்த உறுப்பைக் காண்க: B, D, G, K, P, ?",
         ["T", "U", "V", "W"], 2,
         "இடைவெளி ஒவ்வொரு முறையும் 1 அதிகரிக்கிறது: +2, +3, +4, +5, +6. P+6 = V. முக்கியக் கற்றல் கருத்து: உறுப்புகளுக்கிடையிலான இடைவெளியே சீராக அதிகரிக்கும்போது, அடுத்த உறுப்பைக் காணும் முன் இடைவெளி அமைப்பைக் கண்டறியவும்."),
        # Q16
        ("விடுபட்ட உறுப்பைக் காண்க: AZ, BY, CX, DW, ?",
         ["EV", "EU", "EW", "FV"], 0,
         "முதல் எழுத்து முன்னோக்கி நகர்கிறது (A,B,C,D,E); இரண்டாம் எழுத்து பின்னோக்கி நகர்கிறது (Z,Y,X,W,V). முக்கியக் கற்றல் கருத்து: இரண்டெழுத்துத் தொடர்களில், ஒவ்வோர் இடமும் தனக்கெனத் தனி அமைப்பைப் பின்பற்றுகிறதா எனச் சரிபார்க்கவும்."),
        # Q17
        ("A, B, C, D, E என்ற ஐந்து நண்பர்கள் ஒரு வரிசையில் அமர்ந்துள்ளனர். B, A-க்கு உடனடியாக வலப்புறம் உள்ளார். C, D-க்கு உடனடியாக இடப்புறம் உள்ளார். E, B-க்கும் C-க்கும் இடையில் உள்ளார். A ஒரு முனையில் அமர்ந்தால், மறுமுனையில் அமர்ந்திருப்பவர் யார்?",
         ["B", "C", "D", "E"], 2,
         "வரிசை: A, B, E, C, D. விடை: D. முக்கியக் கற்றல் கருத்து: மிகக் குறிப்பிட்ட நிபந்தனையை (இங்கு, “A ஒரு முனையில்”) முதலில் அமர்த்தி, மீதமுள்ள குறிப்புகளைக் கொண்டு வெளிநோக்கி அமைக்கவும்."),
        # Q18
        ("40 மாணவர்கள் கொண்ட ஒரு வகுப்பில், ராஜ் மேலிருந்து 12-ஆம் இடத்தில் உள்ளார். கீழிருந்து அவரது தரவரிசை என்ன?",
         ["27", "28", "29", "30"], 2,
         "கீழிருந்து தரவரிசை = மொத்தம் − மேலிருந்து தரவரிசை + 1 = 40 − 12 + 1 = 29. முக்கியக் கற்றல் கருத்து: கீழிருந்து தரவரிசை = மொத்த மாணவர்கள் − மேலிருந்து தரவரிசை + 1."),
        # Q19
        ("30 மாணவர்கள் கொண்ட ஒரு வரிசையில், மீனா இடமிருந்து 15-ஆவதாகவும், பிரியா வலமிருந்து 10-ஆவதாகவும் உள்ளனர். அவர்களுக்கிடையே எத்தனை மாணவர்கள் உள்ளனர்?",
         ["4", "5", "6", "7"], 1,
         "இடமிருந்து பிரியாவின் இடம் = 30 − 10 + 1 = 21. 15 மற்றும் 21 ஆகிய இடங்களுக்கிடையே உள்ள மாணவர்கள் = 21 − 15 − 1 = 5. முக்கியக் கற்றல் கருத்து: ஒப்பிடும் முன் அனைத்து இடங்களையும் ஒரே குறிப்புத்திசைக்கு (இடம் அல்லது வலம்) மாற்றவும்."),
        # Q20
        ("FRIEND என்பது HTKGPF என எழுதப்பட்டால், அதே குறியீட்டில் CANDLE எவ்வாறு எழுதப்படும்?",
         ["ECPFNG", "ECPFMG", "EDPFNG", "ECQFNG"], 0,
         "அமைப்பைச் சரிபார்க்க: ஒவ்வோர் எழுத்தும் 2 இடங்கள் முன்னோக்கி நகர்கிறது (F→H, R→T, I→K, E→G, N→P, D→F). CANDLE: C→E, A→C, N→P, D→F, L→N, E→G = ECPFNG. முக்கியக் கற்றல் கருத்து: புதிய சொல்லுக்குப் பயன்படுத்தும் முன், கொடுக்கப்பட்ட எடுத்துக்காட்டின் பல எழுத்துகளைக் கொண்டு நகர்வு மதிப்பை உறுதிசெய்யவும்."),
        # Q21
        ("ஒருவரைச் சுட்டிக்காட்டி ஒரு பெண், “இவரது தாய் என் தாயின் ஒரே மகள்” என்கிறார். அப்பெண் அவருக்கு என்ன உறவு?",
         ["தாய்", "சகோதரி", "பாட்டி", "அத்தை"], 0,
         "அவரது தாயின் ஒரே மகள் = அப்பெண்ணே. எனவே “இவரது தாய்” = அப்பெண் → அவர் இவருடைய தாய். முக்கியக் கற்றல் கருத்து: ஒருவரை “என் பெற்றோரின் ஒரே மகள்/மகன்” என ஒரு குறிப்பு வரையறுக்கும்போது, அது பேசுபவரையே குறிக்கிறதா என முதலில் சரிபார்க்கவும்."),
        # Q22
        ("ஒருவர் வடக்கை நோக்கி நடக்கத் தொடங்குகிறார். அவர் 90° கடிகாரச் சுற்றில், பின்னர் 180°, பின்னர் 90° எதிர்க்கடிகாரச் சுற்றில் திரும்புகிறார். அவர் இப்போது எத்திசையை நோக்கியுள்ளார்?",
         ["வடக்கு", "தெற்கு", "கிழக்கு", "மேற்கு"], 1,
         "வடக்கு → (90° கடிகாரச் சுற்று) → கிழக்கு → (180°) → மேற்கு → (90° எதிர்க்கடிகாரச் சுற்று) → தெற்கு. முக்கியக் கற்றல் கருத்து: மொத்தக் கோணத்தை ஒரே நேரத்தில் கணக்கிட முயலாமல், ஒவ்வொரு திருப்பத்தையும் மனத்திலுள்ள திசைகாட்டியில் படிப்படியாகப் பின்தொடரவும்."),
        # Q23
        ("கூற்றுகள்: எந்த ஆசிரியரும் மாணவர் அல்ல. எல்லா மாணவர்களும் கற்போர். முடிவு: எந்த ஆசிரியரும் கற்பவர் அல்ல. முடிவு பொருந்துமா?",
         ["முடிவு பொருந்துகிறது", "முடிவு பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டு முடிவுகளும் பொருந்துகின்றன"], 1,
         "“எந்த A-யும் B அல்ல” என்பதும் “எல்லா B-யும் C” என்பதும் இணைந்து “எந்த A-யும் C அல்ல” என்பதைச் செல்லத்தக்க வகையில் தராது – ஆசிரியர்கள் வேறு வழியில் கற்போராக இருக்கலாம். முக்கியக் கற்றல் கருத்து: எதிர்மறைக் கூற்றும் (“எந்த A-யும் B அல்ல”) நேர்மறைக் கூற்றும் (“எல்லா B-யும் C”) இணைந்து, A மற்றும் C குறித்து ஒருபோதும் செல்லத்தக்க எதிர்மறை முடிவைத் தருவதில்லை."),
        # Q24
        ("5 : 25 :: 7 : ?",
         ["35", "42", "49", "56"], 2,
         "தொடர்பு “எண்ணின் வர்க்கம்”: 5²=25, எனவே 7²=49. முக்கியக் கற்றல் கருத்து: எண் ஒப்புமைகள் பெரும்பாலும் ஒரு கணிதத் தொடர்பைப் (வர்க்கம், கனம், இருமடங்கு) பயன்படுத்துகின்றன – பயன்படுத்தும் முன் அதை முதல் இணையுடன் சரிபார்க்கவும்."),
        # Q25
        ("P, Q, R, S, T என்ற ஐந்து பெட்டிகள் அடுக்கப்பட்டுள்ளன. P, Q-க்கு நேர்மேலே உள்ளது. Q, R-க்கு நேர்மேலே உள்ளது. S, T-க்கு நேர்மேலே உள்ளது. T அடியில் உள்ளது. மேலிருந்து கீழாக வரிசையைக் காண்க.",
         ["P, Q, R, S, T", "Q, P, R, S, T", "P, Q, S, R, T", "P, R, Q, S, T"], 0,
         "T அடியில் உள்ளது (5-ஆம் இடம்). S, T-க்கு நேர்மேலே உள்ளது (4-ஆம் இடம்). P, Q-க்கு மேலே, Q, R-க்கு மேலே என்பதால் P, Q, R ஆகியவை முறையே 1, 2, 3 ஆகிய இடங்களைப் பெறுகின்றன. முக்கியக் கற்றல் கருத்து: நிலையான குறிப்புப் புள்ளியை (“T அடியில்”) முதலில் அமர்த்தி, பின்னர் மீதமுள்ள அடுக்கை அதைச் சுற்றி அமைக்கவும்.")
    ]

    # 30 Independent Practice (English)
    indep_en = [
        # Q1
        ("In a code, each letter is replaced by the letter in the opposite position of the alphabet (A↔Z, B↔Y, C↔X, …). If DOG is written as WLT, how is CAT written?",
         ["XZG", "XAG", "YZG", "XZH"], 0,
         "Verify: D(4th) → W(4th from the end), O → L, G → T. CAT: C → X, A → Z, T → G = XZG. Key Learning Point: In opposite-letter (reverse alphabet) codes, the positions of a letter and its code add up to 27 (e.g., D = 4, W = 23).", "EASY"),
        # Q2
        ("Pointing to a boy, a man says, “He is the son of my wife’s mother’s only daughter.” How is the boy related to the man?",
         ["Son", "Nephew", "Brother", "Grandson"], 0,
         "Wife’s mother’s only daughter = the man’s wife herself. Son of his wife = his own son. Key Learning Point: Resolve each “only son/daughter” clue one step at a time, starting from the innermost relationship.", "EASY"),
        # Q3
        ("A man walks 4 km South, turns left, walks 4 km. Which direction does he now face?",
         ["North", "South", "East", "West"], 2,
         "Facing South, a left turn faces him East. Key Learning Point: A left turn from South faces East; track turns using a mental compass, not memorised rules alone.", "EASY"),
        # Q4
        ("Pen : Write :: Knife : ?",
         ["Sharp", "Cut", "Kitchen", "Blade"], 1,
         "A pen is used to write; a knife is used to cut. Key Learning Point: Function-based analogies pair an object with its primary use.", "EASY"),
        # Q5
        ("Find the odd one out: Delhi, Mumbai, Chennai, Punjab.",
         ["Delhi", "Mumbai", "Chennai", "Punjab"], 3,
         "Delhi, Mumbai, and Chennai are cities; Punjab is a state. Key Learning Point: Check the category level (city vs. state) rather than just the surface similarity (all place names).", "EASY"),
        # Q6
        ("Find the next term: A, C, E, G, ?",
         ["H", "I", "J", "K"], 1,
         "Pattern: skip one letter each time (+2). G+2 = I. Key Learning Point: A constant gap between terms is the simplest series pattern to check first.", "EASY"),
        # Q7
        ("If LAMP is coded as MZNO, how is DESK coded in the same way?",
         ["EDTJ", "EFTL", "CDRJ", "EDTL"], 0,
         "Verify: L→M (+1), A→Z (−1), M→N (+1), P→O (−1) – the shift alternates +1, −1. DESK: D→E (+1), E→D (−1), S→T (+1), K→J (−1) = EDTJ. Key Learning Point: Check the shift of every letter separately – the shift may alternate rather than stay the same.", "EASY"),
        # Q8
        ("A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?",
         ["Uncle", "Father", "Grandfather", "Cousin"], 0,
         "A, B, and C are siblings (A is B’s brother, B is C’s sister). C is D’s father, so A is D’s uncle. Key Learning Point: Once siblings are identified, a sibling’s child is always a niece/nephew relationship to the other siblings.", "MEDIUM"),
        # Q9
        ("A man walks 5 km West, 5 km South, 5 km East. How far is he from the start, and in which direction?",
         ["5 km North", "5 km South", "10 km South", "0 km"], 1,
         "West and East cancel out, leaving only the 5 km South displacement. Key Learning Point: Always cancel opposite-direction movements before computing the net displacement.", "EASY"),
        # Q10
        ("A man is facing North-West. He turns 90° clockwise and then 135° anticlockwise. Which direction is he facing now?",
         ["West", "South-West", "North", "South"], 0,
         "North-West → (90° clockwise) → North-East. North-East → (135° anticlockwise) → North → North-West → West. Key Learning Point: For turns of 45° multiples, move one compass point (N, NE, E, …) for every 45° in the direction of the turn.", "MEDIUM"),
        # Q11
        ("Statements: All doctors are educated. Some educated are rich. Conclusion: Some doctors are rich. Does the conclusion follow?",
         ["Follows", "Does not follow", "Cannot be determined", "Both follow"], 1,
         "“All A are B” combined with “Some B are C” does not guarantee “Some A are C,” since the “rich” subset of educated people may not include any doctors. Key Learning Point: “All A are B” + “Some B are C” is not a valid combination for concluding “Some A are C.”", "MEDIUM"),
        # Q12
        ("Statements: Some books are novels. No novels are magazines. Conclusions: I. Some books are not magazines. II. No books are magazines. Which follow(s)?",
         ["Only I follows", "Only II follows", "Both follow", "Neither follows"], 0,
         "I follows: the books that are novels cannot be magazines, so some books are not magazines. II does not follow: books that are not novels may or may not be magazines. Key Learning Point: “Some A are B” combined with “No B are C” always gives “Some A are not C,” but never “No A are C.”", "MEDIUM"),
        # Q13
        ("Author : Book :: Sculptor : ?",
         ["Chisel", "Statue", "Museum", "Stone"], 1,
         "An author creates a book; a sculptor creates a statue. Key Learning Point: Creator-creation analogies pair a person with what they produce, not the tool they use.", "EASY"),
        # Q14
        ("Find the odd one out: Guitar, Violin, Sitar, Flute.",
         ["Guitar", "Violin", "Sitar", "Flute"], 3,
         "Guitar, Violin, and Sitar are string instruments; Flute is a wind instrument. Key Learning Point: Group items by their underlying mechanism, not just their broad category (all being “instruments”).", "EASY"),
        # Q15
        ("Find the next term: Z, X, U, Q, ?",
         ["K", "L", "M", "N"], 1,
         "Gap increases each time: −2, −3, −4, −5. Q−5 = L. Key Learning Point: A steadily increasing (or decreasing) gap is a common HOTS-level series pattern.", "EASY"),
        # Q16
        ("Find the missing term: AB, DE, GH, JK, ?",
         ["MN", "LM", "MO", "NM"], 0,
         "First letter of each pair moves forward by 3 (A,D,G,J,M); second letter is always one ahead of the first. Key Learning Point: In paired-letter series, check the gap within each pair separately from the gap between pairs.", "EASY"),
        # Q17
        ("Six friends P, Q, R, S, T, U sit in a row. Q is 2nd from the left. T is immediately right of Q. R is at the extreme right. S is immediately left of R. P is between T and S. Find U’s position.",
         ["1st", "2nd", "5th", "6th"], 0,
         "Q=2nd, T=3rd, R=6th, S=5th, P=4th (between T and S). Remaining position 1 = U. Key Learning Point: Fill in the fixed positions first (extreme ends), then work inward with the relative clues.", "MEDIUM"),
        # Q18
        ("In a class, Anu ranks 8th from the top and 25th from the bottom. How many students are in the class?",
         ["30", "31", "32", "33"], 2,
         "Total = 8 + 25 − 1 = 32. Key Learning Point: Total = rank from top + rank from bottom − 1, since the person is counted in both ranks.", "EASY"),
        # Q19
        ("In a row of 25 trees, a tree is 9th from the left end. What is its position from the right end?",
         ["15", "16", "17", "18"], 2,
         "Position from right = 25 − 9 + 1 = 17. Key Learning Point: Position from the other end = Total − position from this end + 1.", "EASY"),
        # Q20
        ("If DOG is coded as CNF, how is HEN coded in the same way?",
         ["GDM", "IFO", "GEM", "GDN"], 0,
         "Verify pattern: D→C, O→N, G→F – each letter shifts backward by 1. HEN: H→G, E→D, N→M = GDM. Key Learning Point: Codes can shift letters backward as well as forward – check the direction of the shift in the given example.", "EASY"),
        # Q21
        ("A woman introduces a man as “the son of my mother’s only daughter’s husband.” How is the man related to the woman?",
         ["Son", "Husband", "Brother", "Nephew"], 0,
         "Mother’s only daughter = the woman herself. Her husband’s son = her own son. Key Learning Point: Resolve nested clues from the innermost relationship outward.", "EASY"),
        # Q22
        ("A person starts facing East, turns 90° anticlockwise, then 90° anticlockwise again, then 90° clockwise. Which direction now?",
         ["North", "South", "East", "West"], 0,
         "East → (ACW) → North → (ACW) → West → (CW) → North. Key Learning Point: Track each turn one at a time on a mental compass rather than summing angles first.", "EASY"),
        # Q23
        ("Statements: Some fruits are sweet. All sweet things are liked by children. Conclusion: Some fruits are liked by children. Does the conclusion follow?",
         ["Follows", "Does not follow", "Cannot be determined", "Both follow"], 0,
         "“Some A are B” + “All B are C” validly gives “Some A are C.” Key Learning Point: “Some A are B” combined with “All B are C” is a valid pattern for concluding “Some A are C.”", "EASY"),
        # Q24
        ("8 : 64 :: 9 : ?",
         ["81", "512", "729", "648"], 0,
         "The relationship is “square of the number”: 8²=64, so 9²=81. Key Learning Point: Check the exact relationship (square vs. cube) using the first pair before assuming a pattern.", "EASY"),
        # Q25
        ("Four boxes W, X, Y, Z are stacked such that W is above X, X is above Y, and Z is at the bottom, directly below Y. Find the order top to bottom.",
         ["W, X, Y, Z", "X, W, Y, Z", "W, Y, X, Z", "D. Y, X, W, Z"], 0,
         "W above X above Y above Z, in that order. Key Learning Point: Chain the “above” relationships in sequence to build the full order.", "EASY"),
        # Q26
        ("Village P is to the North of Village Q. Village R is to the East of Village Q. In which direction is P with respect to R?",
         ["North-East", "North-West", "South-East", "South-West"], 1,
         "Place Q at the centre: P is above Q (North) and R is to the right of Q (East). From R, P lies upward and to the left – that is, North-West. Key Learning Point: For relative-direction questions, draw a quick sketch from a common reference point, then read the direction from the place asked about.", "MEDIUM"),
        # Q27
        ("A’s father is B. B’s sister is C. C’s son is D. How is D related to A?",
         ["Cousin", "Brother", "Uncle", "Nephew"], 0,
         "B and C are siblings. C’s son D is B’s nephew, and since A is B’s child, D is A’s cousin. Key Learning Point: A parent’s sibling’s child is always a cousin.", "MEDIUM"),
        # Q28
        ("Statements: All pens are pencils. No pencils are erasers. Conclusion: No pens are erasers. Does the conclusion follow?",
         ["Follows", "Does not follow", "Cannot be determined", "Both follow"], 0,
         "“All A are B” + “No B are C” validly gives “No A are C.” Key Learning Point: “All A are B” combined with “No B are C” is a valid pattern for concluding “No A are C” – unlike the reverse order.", "EASY"),
        # Q29
        ("Find the missing term: BCE, DEG, FGI, ?",
         ["HIK", "HIJ", "GIK", "HJK"], 0,
         "Start letters go B, D, F, H (+2 each); each group is (start, start+1, start+3). Key Learning Point: Break a multi-letter series into its starting-letter pattern and its internal (within-group) pattern separately.", "EASY"),
        # Q30
        ("In a row of 35 students, Kavin is 10th from the left and Mala is 12th from the right. How many students are between them?",
         ["12", "13", "14", "15"], 1,
         "Mala’s position from the left = 35 − 12 + 1 = 24. Students between positions 10 and 24 = 24 − 10 − 1 = 13. Key Learning Point: To count people between two positions, convert both positions to the same end first, then subtract and take away 1.", "MEDIUM")
    ]

    # 30 Independent Practice (Tamil)
    indep_ta = [
        # Q1
        ("ஒரு குறியீட்டில், ஒவ்வோர் எழுத்தும் அகரவரிசையின் எதிர் இடத்திலுள்ள எழுத்தால் மாற்றப்படுகிறது (A↔Z, B↔Y, C↔X, …). DOG என்பது WLT என எழுதப்பட்டால், CAT எவ்வாறு எழுதப்படும்?",
         ["XZG", "XAG", "YZG", "XZH"], 0,
         "சரிபார்க்க: D (4-ஆவது) → W (இறுதியிலிருந்து 4-ஆவது), O → L, G → T. CAT: C → X, A → Z, T → G = XZG. முக்கியக் கற்றல் கருத்து: எதிர் எழுத்து (தலைகீழ் அகரவரிசை) குறியீடுகளில், ஓர் எழுத்தின் இட எண்ணும் அதன் குறியீட்டின் இட எண்ணும் சேர்ந்து 27 ஆகும் (எ.கா., D = 4, W = 23)."),
        # Q2
        ("ஒரு சிறுவனைச் சுட்டிக்காட்டி ஒருவர், “இவன் என் மனைவியின் தாயின் ஒரே மகளின் மகன்” என்கிறார். அச்சிறுவன் அவருக்கு என்ன உறவு?",
         ["மகன்", "மருமகன் (உடன்பிறந்தவரின் மகன்)", "சகோதரர்", "பேரன்"], 0,
         "மனைவியின் தாயின் ஒரே மகள் = அவரது மனைவியே. அவரது மனைவியின் மகன் = அவருடைய சொந்த மகன். முக்கியக் கற்றல் கருத்து: ஒவ்வொரு “ஒரே மகன்/மகள்” குறிப்பையும் உள்ளார்ந்த உறவிலிருந்து தொடங்கி ஒவ்வொரு படியாகத் தீர்க்கவும்."),
        # Q3
        ("ஒருவர் 4 கி.மீ தெற்கே நடந்து, இடப்புறம் திரும்பி, 4 கி.மீ நடக்கிறார். அவர் இப்போது எத்திசையை நோக்கியுள்ளார்?",
         ["வடக்கு", "தெற்கு", "கிழக்கு", "மேற்கு"], 2,
         "தெற்கை நோக்கியிருக்கும்போது இடப்புறம் திரும்பினால் கிழக்கை நோக்குவார். முக்கியக் கற்றல் கருத்து: தெற்கிலிருந்து இடப்புறத் திருப்பம் கிழக்கை நோக்கும்; மனப்பாட விதிகளை மட்டும் நம்பாமல், மனத்திலுள்ள திசைகாட்டியைக் கொண்டு திருப்பங்களைப் பின்தொடரவும்."),
        # Q4
        ("பேனா : எழுது :: கத்தி : ?",
         ["கூர்மை", "வெட்டு", "சமையலறை", "அலகு"], 1,
         "பேனா எழுதப் பயன்படுகிறது; கத்தி வெட்டப் பயன்படுகிறது. முக்கியக் கற்றல் கருத்து: பயன்பாட்டு அடிப்படையிலான ஒப்புமைகள் ஒரு பொருளை அதன் முதன்மைப் பயன்பாட்டுடன் இணைக்கின்றன."),
        # Q5
        ("பொருந்தாததைக் கண்டறிக: டெல்லி, மும்பை, சென்னை, பஞ்சாப்.",
         ["டெல்லி", "மும்பை", "சென்னை", "பஞ்சாப்"], 3,
         "டெல்லி, மும்பை, சென்னை ஆகியவை நகரங்கள்; பஞ்சாப் ஒரு மாநிலம். முக்கியக் கற்றல் கருத்து: மேலோட்டமான ஒற்றுமையை (அனைத்தும் இடப்பெயர்கள்) மட்டும் பார்க்காமல், வகைமை நிலையை (நகரம் / மாநிலம்) சரிபார்க்கவும்."),
        # Q6
        ("அடுத்த உறுப்பைக் காண்க: A, C, E, G, ?",
         ["H", "I", "J", "K"], 1,
         "அமைப்பு: ஒவ்வொரு முறையும் ஓர் எழுத்தைத் தவிர்க்கவும் (+2). G+2 = I. முக்கியக் கற்றல் கருத்து: உறுப்புகளுக்கிடையிலான மாறா இடைவெளியே முதலில் சரிபார்க்க வேண்டிய எளிய தொடர் அமைப்பு."),
        # Q7
        ("LAMP என்பது MZNO எனக் குறியிடப்பட்டால், அதே முறையில் DESK எவ்வாறு குறியிடப்படும்?",
         ["EDTJ", "EFTL", "CDRJ", "EDTL"], 0,
         "சரிபார்க்க: L→M (+1), A→Z (−1), M→N (+1), P→O (−1) – நகர்வு +1, −1 என மாறி மாறி வருகிறது. DESK: D→E (+1), E→D (−1), S→T (+1), K→J (−1) = EDTJ. முக்கியக் கற்றல் கருத்து: ஒவ்வோர் எழுத்தின் நகர்வையும் தனித்தனியாகச் சரிபார்க்கவும் – நகர்வு ஒரே மாதிரியாக இல்லாமல் மாறி மாறி வரலாம்."),
        # Q8
        ("A என்பவர் B-இன் சகோதரர். B என்பவர் C-இன் சகோதரி. C என்பவர் D-இன் தந்தை. A என்பவர் D-க்கு என்ன உறவு?",
         ["தந்தையின் சகோதரர்", "தந்தை", "தாத்தா", "ஒன்றுவிட்ட உடன்பிறப்பு (Cousin)"], 0,
         "A, B, C ஆகியோர் உடன்பிறந்தவர்கள் (A, B-இன் சகோதரர்; B, C-இன் சகோதரி). C, D-இன் தந்தை; எனவே A, D-இன் தந்தையின் சகோதரர் (Uncle). முக்கியக் கற்றல் கருத்து: உடன்பிறந்தோர் அடையாளம் காணப்பட்டதும், ஓர் உடன்பிறந்தவரின் பிள்ளை மற்ற உடன்பிறந்தோருக்கு எப்போதும் மருமகன்/மருமகள் உறவாகும்."),
        # Q9
        ("ஒருவர் 5 கி.மீ மேற்கே, 5 கி.மீ தெற்கே, 5 கி.மீ கிழக்கே நடக்கிறார். அவர் தொடக்கத்திலிருந்து எவ்வளவு தூரத்தில், எத்திசையில் உள்ளார்?",
         ["5 கி.மீ வடக்கு", "5 கி.மீ தெற்கு", "10 கி.மீ தெற்கு", "0 கி.மீ"], 1,
         "மேற்கும் கிழக்கும் ஒன்றையொன்று நீக்குகின்றன; 5 கி.மீ தெற்கு இடப்பெயர்ச்சி மட்டுமே மீதமுள்ளது. முக்கியக் கற்றல் கருத்து: நிகர இடப்பெயர்ச்சியைக் கணக்கிடும் முன் எப்போதும் எதிர்த்திசை நகர்வுகளை நீக்கவும்."),
        # Q10
        ("ஒருவர் வடமேற்கை நோக்கியுள்ளார். அவர் 90° கடிகாரச் சுற்றிலும், பின்னர் 135° எதிர்க்கடிகாரச் சுற்றிலும் திரும்புகிறார். அவர் இப்போது எத்திசையை நோக்கியுள்ளார்?",
         ["மேற்கு", "தென்மேற்கு", "வடக்கு", "தெற்கு"], 0,
         "வடமேற்கு → (90° கடிகாரச் சுற்று) → வடகிழக்கு. வடகிழக்கு → (135° எதிர்க்கடிகாரச் சுற்று) → வடக்கு → வடமேற்கு → மேற்கு. முக்கியக் கற்றல் கருத்து: 45°-இன் மடங்குகளாக உள்ள திருப்பங்களுக்கு, ஒவ்வொரு 45°-க்கும் திருப்பத்தின் திசையில் ஒரு திசைப் புள்ளி (வ, வகி, கி, …) நகரவும்."),
        # Q11
        ("கூற்றுகள்: எல்லா மருத்துவர்களும் கல்வியறிவு பெற்றவர்கள். கல்வியறிவு பெற்றவர்களில் சிலர் செல்வந்தர்கள். முடிவு: சில மருத்துவர்கள் செல்வந்தர்கள். முடிவு பொருந்துமா?",
         ["பொருந்துகிறது", "பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டும் பொருந்துகின்றன"], 1,
         "“எல்லா A-யும் B” என்பதும் “சில B, C” என்பதும் இணைந்து “சில A, C” என்பதை உறுதிசெய்யாது; கல்வியறிவு பெற்றவர்களில் உள்ள “செல்வந்தர்” பகுதியில் மருத்துவர் யாரும் இல்லாமலும் இருக்கலாம். முக்கியக் கற்றல் கருத்து: “எல்லா A-யும் B” + “சில B, C” என்பது “சில A, C” என முடிவு செய்வதற்குச் செல்லத்தக்க இணைப்பு அல்ல."),
        # Q12
        ("கூற்றுகள்: சில புத்தகங்கள் நாவல்கள். எந்த நாவலும் இதழ் அல்ல. முடிவுகள்: I. சில புத்தகங்கள் இதழ்கள் அல்ல. II. எந்தப் புத்தகமும் இதழ் அல்ல. எது/எவை பொருந்தும்?",
         ["I மட்டும் பொருந்துகிறது", "II மட்டும் பொருந்துகிறது", "இரண்டும் பொருந்துகின்றன", "எதுவும் பொருந்தவில்லை"], 0,
         "I பொருந்துகிறது: நாவல்களாக உள்ள புத்தகங்கள் இதழ்களாக இருக்க முடியாது; எனவே சில புத்தகங்கள் இதழ்கள் அல்ல. II பொருந்தவில்லை: நாவல்கள் அல்லாத புத்தகங்கள் இதழ்களாக இருக்கலாம் அல்லது இல்லாமலும் இருக்கலாம். முக்கியக் கற்றல் கருத்து: “சில A, B” என்பதும் “எந்த B-யும் C அல்ல” என்பதும் இணைந்தால் எப்போதும் “சில A, C அல்ல” கிடைக்கும்; ஆனால் ஒருபோதும் “எந்த A-யும் C அல்ல” கிடைக்காது."),
        # Q13
        ("எழுத்தாளர் : புத்தகம் :: சிற்பி : ?",
         ["உளி", "சிலை", "அருங்காட்சியகம்", "கல்"], 1,
         "எழுத்தாளர் புத்தகத்தை உருவாக்குகிறார்; சிற்பி சிலையை உருவாக்குகிறார். முக்கியக் கற்றல் கருத்து: படைப்பாளர்–படைப்பு ஒப்புமைகள் ஒருவரை அவர் பயன்படுத்தும் கருவியுடன் அல்லாமல், அவர் உருவாக்குவதுடன் இணைக்கின்றன."),
        # Q14
        ("பொருந்தாததைக் கண்டறிக: கிட்டார், வயலின், சிதார், புல்லாங்குழல்.",
         ["கிட்டார்", "வயலின்", "சிதார்", "புல்லாங்குழல்"], 3,
         "கிட்டார், வயலின், சிதார் ஆகியவை நரம்பிசைக் கருவிகள்; புல்லாங்குழல் ஒரு காற்றிசைக் கருவி. முக்கியக் கற்றல் கருத்து: பரந்த வகைமையை (அனைத்தும் “இசைக் கருவிகள்”) மட்டும் பார்க்காமல், அடிப்படைச் செயல்முறையின்படி உருப்படிகளைக் குழுவாக்கவும்."),
        # Q15
        ("அடுத்த உறுப்பைக் காண்க: Z, X, U, Q, ?",
         ["K", "L", "M", "N"], 1,
         "இடைவெளி ஒவ்வொரு முறையும் அதிகரிக்கிறது: −2, −3, −4, −5. Q−5 = L. முக்கியக் கற்றல் கருத்து: சீராக அதிகரிக்கும் (அல்லது குறையும்) இடைவெளி ஒரு பொதுவான உயர்நிலைத் தொடர் அமைப்பாகும்."),
        # Q16
        ("விடுபட்ட உறுப்பைக் காண்க: AB, DE, GH, JK, ?",
         ["MN", "LM", "MO", "NM"], 0,
         "ஒவ்வோர் இணையின் முதல் எழுத்தும் 3 இடங்கள் முன்னோக்கி நகர்கிறது (A,D,G,J,M); இரண்டாம் எழுத்து எப்போதும் முதல் எழுத்தைவிட ஓரிடம் முன்னால் உள்ளது. முக்கியக் கற்றல் கருத்து: இணை எழுத்துத் தொடர்களில், ஓர் இணைக்குள் உள்ள இடைவெளியையும் இணைகளுக்கிடையிலான இடைவெளியையும் தனித்தனியாகச் சரிபார்க்கவும்."),
        # Q17
        ("P, Q, R, S, T, U என்ற ஆறு நண்பர்கள் ஒரு வரிசையில் அமர்ந்துள்ளனர். Q இடமிருந்து 2-ஆவது இடத்தில் உள்ளார். T, Q-க்கு உடனடியாக வலப்புறம் உள்ளார். R வலது ஓரத்தில் உள்ளார். S, R-க்கு உடனடியாக இடப்புறம் உள்ளார். P, T-க்கும் S-க்கும் இடையில் உள்ளார். U-இன் இடத்தைக் காண்க.",
         ["1-ஆவது", "2-ஆவது", "5-ஆவது", "6-ஆவது"], 0,
         "Q=2-ஆவது, T=3-ஆவது, R=6-ஆவது, S=5-ஆவது, P=4-ஆவது (T-க்கும் S-க்கும் இடையில்). மீதமுள்ள 1-ஆவது இடம் = U. முக்கியக் கற்றல் கருத்து: முதலில் நிலையான இடங்களை (ஓரங்கள்) நிரப்பி, பின்னர் சார்புக் குறிப்புகளைக் கொண்டு உள்நோக்கிச் செயல்படவும்."),
        # Q18
        ("ஒரு வகுப்பில், அனு மேலிருந்து 8-ஆவதாகவும் கீழிருந்து 25-ஆவதாகவும் உள்ளார். வகுப்பில் எத்தனை மாணவர்கள் உள்ளனர்?",
         ["30", "31", "32", "33"], 2,
         "மொத்தம் = 8 + 25 − 1 = 32. முக்கியக் கற்றல் கருத்து: அந்நபர் இரண்டு தரவரிசைகளிலும் எண்ணப்படுவதால், மொத்தம் = மேலிருந்து தரவரிசை + கீழிருந்து தரவரிசை − 1."),
        # Q19
        ("25 மரங்கள் கொண்ட ஒரு வரிசையில், ஒரு மரம் இடது முனையிலிருந்து 9-ஆவதாக உள்ளது. வலது முனையிலிருந்து அதன் இடம் என்ன?",
         ["15", "16", "17", "18"], 2,
         "வலமிருந்து இடம் = 25 − 9 + 1 = 17. முக்கியக் கற்றல் கருத்து: மறுமுனையிலிருந்து இடம் = மொத்தம் − இம்முனையிலிருந்து இடம் + 1."),
        # Q20
        ("DOG என்பது CNF எனக் குறியிடப்பட்டால், அதே முறையில் HEN எவ்வாறு குறியிடப்படும்?",
         ["GDM", "IFO", "GEM", "GDN"], 0,
         "அமைப்பைச் சரிபார்க்க: D→C, O→N, G→F – ஒவ்வோர் எழுத்தும் 1 இடம் பின்னோக்கி நகர்கிறது. HEN: H→G, E→D, N→M = GDM. முக்கியக் கற்றல் கருத்து: குறியீடுகள் எழுத்துகளை முன்னோக்கி மட்டுமல்லாமல் பின்னோக்கியும் நகர்த்தலாம் – கொடுக்கப்பட்ட எடுத்துக்காட்டில் நகர்வின் திசையைச் சரிபார்க்கவும்."),
        # Q21
        ("ஒரு பெண் ஒருவரை “என் தாயின் ஒரே மகளின் கணவரின் மகன்” என அறிமுகப்படுத்துகிறார். அவர் அப்பெண்ணுக்கு என்ன உறவு?",
         ["மகன்", "கணவர்", "சகோதரர்", "மருமகன் (உடன்பிறந்தவரின் மகன்)"], 0,
         "தாயின் ஒரே மகள் = அப்பெண்ணே. அவரது கணவரின் மகன் = அவருடைய சொந்த மகன். முக்கியக் கற்றல் கருத்து: உள்ளடங்கிய குறிப்புகளை உள்ளார்ந்த உறவிலிருந்து வெளிநோக்கித் தீர்க்கவும்."),
        # Q22
        ("ஒருவர் கிழக்கை நோக்கித் தொடங்கி, 90° எதிர்க்கடிகாரச் சுற்றில், மீண்டும் 90° எதிர்க்கடிகாரச் சுற்றில், பின்னர் 90° கடிகாரச் சுற்றில் திரும்புகிறார். இப்போது எத்திசை?",
         ["வடக்கு", "தெற்கு", "கிழக்கு", "மேற்கு"], 0,
         "கிழக்கு → (எதிர்க்கடிகாரம்) → வடக்கு → (எதிர்க்கடிகாரம்) → மேற்கு → (கடிகாரம்) → வடக்கு. முக்கியக் கற்றல் கருத்து: கோணங்களை முதலில் கூட்டாமல், ஒவ்வொரு திருப்பத்தையும் மனத்திலுள்ள திசைகாட்டியில் ஒவ்வொன்றாகப் பின்தொடரவும்."),
        # Q23
        ("கூற்றுகள்: சில பழங்கள் இனிப்பானவை. எல்லா இனிப்புப் பொருட்களும் குழந்தைகளுக்குப் பிடிக்கும். முடிவு: சில பழங்கள் குழந்தைகளுக்குப் பிடிக்கும். முடிவு பொருந்துமா?",
         ["பொருந்துகிறது", "பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டும் பொருந்துகின்றன"], 0,
         "“சில A, B” + “எல்லா B-யும் C” செல்லத்தக்க வகையில் “சில A, C” எனத் தருகிறது. முக்கியக் கற்றல் கருத்து: “சில A, B” என்பதும் “எல்லா B-யும் C” என்பதும் இணைவது “சில A, C” என முடிவு செய்வதற்கான செல்லத்தக்க அமைப்பாகும்."),
        # Q24
        ("8 : 64 :: 9 : ?",
         ["81", "512", "729", "648"], 0,
         "தொடர்பு “எண்ணின் வர்க்கம்”: 8²=64, எனவே 9²=81. முக்கியக் கற்றல் கருத்து: ஓர் அமைப்பைக் கருதும் முன், முதல் இணையைக்கொண்டு சரியான தொடர்பைச் (வர்க்கமா, கனமா) சரிபார்க்கவும்."),
        # Q25
        ("W, X, Y, Z என்ற நான்கு பெட்டிகள் அடுக்கப்பட்டுள்ளன: W, X-க்கு மேலே; X, Y-க்கு மேலே; Z அடியில், Y-க்கு நேர்கீழே உள்ளது. மேலிருந்து கீழாக வரிசையைக் காண்க.",
         ["W, X, Y, Z", "X, W, Y, Z", "W, Y, X, Z", "Y, X, W, Z"], 0,
         "W, X-க்கு மேலே; X, Y-க்கு மேலே; Y, Z-க்கு மேலே – அவ்வரிசையில். முக்கியக் கற்றல் கருத்து: “மேலே” என்ற தொடர்புகளை வரிசையாக இணைத்து முழு வரிசையை அமைக்கவும்."),
        # Q26
        ("கிராமம் P, கிராமம் Q-க்கு வடக்கே உள்ளது. கிராமம் R, கிராமம் Q-க்குக் கிழக்கே உள்ளது. R-ஐப் பொறுத்து P எத்திசையில் உள்ளது?",
         ["வடகிழக்கு", "வடமேற்கு", "தென்கிழக்கு", "தென்மேற்கு"], 1,
         "Q-ஐ மையத்தில் வைக்கவும்: P, Q-க்கு மேலே (வடக்கு); R, Q-க்கு வலப்புறம் (கிழக்கு). R-இலிருந்து பார்த்தால் P மேல்நோக்கியும் இடப்புறமும் உள்ளது – அதாவது வடமேற்கு. முக்கியக் கற்றல் கருத்து: சார்புத் திசை வினாக்களுக்கு, ஒரு பொதுக் குறிப்புப் புள்ளியிலிருந்து விரைவான வரைபடம் வரைந்து, கேட்கப்பட்ட இடத்திலிருந்து திசையைப் படிக்கவும்."),
        # Q27
        ("A-இன் தந்தை B. B-இன் சகோதரி C. C-இன் மகன் D. D என்பவர் A-க்கு என்ன உறவு?",
         ["ஒன்றுவிட்ட உடன்பிறப்பு (Cousin)", "சகோதரர்", "மாமா / சித்தப்பா", "மருமகன் (உடன்பிறந்தவரின் மகன்)"], 0,
         "B-யும் C-யும் உடன்பிறந்தவர்கள். C-இன் மகன் D, B-இன் மருமகன்; A, B-இன் பிள்ளை என்பதால், D என்பவர் A-இன் ஒன்றுவிட்ட உடன்பிறப்பு (Cousin). முக்கியக் கற்றல் கருத்து: பெற்றோரின் உடன்பிறந்தவரின் பிள்ளை எப்போதும் ஒன்றுவிட்ட உடன்பிறப்பு (Cousin) ஆவார்."),
        # Q28
        ("கூற்றுகள்: எல்லாப் பேனாக்களும் பென்சில்கள். எந்தப் பென்சிலும் அழிப்பான் அல்ல. முடிவு: எந்தப் பேனாவும் அழிப்பான் அல்ல. முடிவு பொருந்துமா?",
         ["பொருந்துகிறது", "பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டும் பொருந்துகின்றன"], 0,
         "“எல்லா A-யும் B” + “எந்த B-யும் C அல்ல” செல்லத்தக்க வகையில் “எந்த A-யும் C அல்ல” எனத் தருகிறது. முக்கியக் கற்றல் கருத்து: “எல்லா A-யும் B” என்பதும் “எந்த B-யும் C அல்ல” என்பதும் இணைவது “எந்த A-யும் C அல்ல” என முடிவு செய்வதற்கான செல்லத்தக்க அமைப்பாகும் – தலைகீழ் வரிசையில் இது பொருந்தாது."),
        # Q29
        ("விடுபட்ட உறுப்பைக் காண்க: BCE, DEG, FGI, ?",
         ["HIK", "HIJ", "GIK", "HJK"], 0,
         "தொடக்க எழுத்துகள் B, D, F, H (ஒவ்வொன்றும் +2); ஒவ்வொரு குழுவும் (தொடக்கம், தொடக்கம்+1, தொடக்கம்+3) என அமைகிறது. முக்கியக் கற்றல் கருத்து: பல எழுத்துத் தொடரை அதன் தொடக்க எழுத்து அமைப்பு மற்றும் குழுவுக்குள் உள்ள அமைப்பு எனத் தனித்தனியாகப் பிரிக்கவும்."),
        # Q30
        ("35 மாணவர்கள் கொண்ட ஒரு வரிசையில், கவின் இடமிருந்து 10-ஆவதாகவும் மாலா வலமிருந்து 12-ஆவதாகவும் உள்ளனர். அவர்களுக்கிடையே எத்தனை மாணவர்கள் உள்ளனர்?",
         ["12", "13", "14", "15"], 1,
         "இடமிருந்து மாலாவின் இடம் = 35 − 12 + 1 = 24. 10 மற்றும் 24 ஆகிய இடங்களுக்கிடையே உள்ள மாணவர்கள் = 24 − 10 − 1 = 13. முக்கியக் கற்றல் கருத்து: இரண்டு இடங்களுக்கிடையே உள்ளவர்களை எண்ண, முதலில் இரு இடங்களையும் ஒரே முனைக்கு மாற்றி, கழித்து, பின்னர் 1-ஐக் கழிக்கவும்.")
    ]

    # 30 Assessment Questions (English)
    assess_en = [
        # Q1
        ("If GARDEN is written as NEDRAG, how is FLOWER written in the same code?",
         ["REWOLF", "REWOFL", "RWEOLF", "FLOWRE"], 0,
         "GARDEN written backwards is NEDRAG – the code simply reverses the order of the letters. FLOWER reversed = REWOLF. Key Learning Point: Not every code is a letter shift – check whether the letters have simply been rearranged (here, reversed) before looking for a shift.", "EASY"),
        # Q2
        ("Pointing to a girl, a man says, “She is the daughter of my son.” How is she related to him?",
         ["Daughter", "Granddaughter", "Niece", "Sister"], 1,
         "The daughter of his son is his son’s child, one generation below his son. So she is his granddaughter. Key Learning Point: A son’s or daughter’s child is always a grandchild – count the generations between the two people.", "EASY"),
        # Q3
        ("At sunrise, Kumar stands facing his own shadow. Which direction is he facing?",
         ["North", "South", "East", "West"], 3,
         "At sunrise, the Sun is in the East, so shadows fall towards the West. Facing his shadow, Kumar faces West. Key Learning Point: In shadow questions, fix the Sun’s position first (East in the morning, West in the evening); the shadow always falls on the opposite side.", "EASY"),
        # Q4
        ("Cow : Calf :: Dog : ?",
         ["Kitten", "Puppy", "Cub", "Foal"], 1,
         "A calf is the young one of a cow; a puppy is the young one of a dog. Key Learning Point: Adult–young analogies pair an animal with the specific name of its young; check that the second pair shows exactly the same relationship.", "EASY"),
        # Q5
        ("Find the odd one out: Cow, Goat, Sheep, Tiger.",
         ["Cow", "Goat", "Sheep", "Tiger"], 3,
         "Cow, Goat, and Sheep are domestic herbivores; Tiger is a wild carnivore. Key Learning Point: Look for the feature shared by most items (domestic, plant-eating) to isolate the one that does not belong.", "EASY"),
        # Q6
        ("Find the next term: D, F, H, J, ?",
         ["K", "L", "M", "N"], 1,
         "Pattern: skip one letter each time (+2): D, F, H, J. J + 2 = L. Key Learning Point: Check for a constant gap between letters first; it is the simplest letter-series pattern.", "EASY"),
        # Q7
        ("If A = 1, B = 2, C = 3, … Z = 26 and CAT = 24, then DOG = ?",
         ["24", "25", "26", "27"], 2,
         "Verify with CAT: C(3) + A(1) + T(20) = 24, so the code is the sum of the letters’ positions. DOG: D(4) + O(15) + G(7) = 26. Key Learning Point: In letter-to-number codes, confirm the rule (sum, product, or reverse position) with the given example before applying it.", "EASY"),
        # Q8
        ("A is B’s sister. C is B’s mother. D is C’s father. How is A related to D?",
         ["Granddaughter", "Daughter", "Niece", "Grandson"], 0,
         "C is B’s mother; A is B’s sister, so C is also A’s mother. D is C’s father, so D is A’s maternal grandfather. A is female (a sister), so A is D’s granddaughter. Key Learning Point: Read the direction of the question carefully – “How is A related to D?” must be answered from A’s side, using A’s gender.", "MEDIUM"),
        # Q9
        ("A man walks 5 km North, then 3 km East, then 9 km South. How far is he from the starting point, and in which direction?",
         ["5 km South-East", "5 km North-East", "7 km South-East", "4 km South"], 0,
         "North–South: 5 km North and 9 km South leave a net 4 km South. East–West: 3 km East. Distance = √(4² + 3²) = √25 = 5 km, towards the South-East. Key Learning Point: First cancel opposite movements, then combine the remaining perpendicular legs using the Pythagorean relationship; the direction comes from those two legs.", "MEDIUM"),
        # Q10
        ("If South-East becomes North, what will West become?",
         ["North-East", "South-East", "North-West", "South"], 1,
         "South-East to North is a turn of 135° anticlockwise. Turning West 135° anticlockwise: West → South-West → South → South-East. Key Learning Point: In direction-rotation questions, find the angle and sense of the turn from the given pair, then apply the same turn to the new direction.", "MEDIUM"),
        # Q11
        ("Statements: All mangoes are fruits. All fruits are healthy. Conclusion: All mangoes are healthy. Does the conclusion follow?",
         ["Follows", "Does not follow", "Cannot be determined", "Both follow"], 0,
         "All mangoes are fruits and all fruits are healthy, so all mangoes are healthy (All A are B + All B are C → All A are C). Key Learning Point: A chain of two “All” statements always gives a valid “All” conclusion.", "EASY"),
        # Q12
        ("Statements: Some students are athletes. All athletes are fit. Conclusions: I. Some students are fit. II. All students are fit. Which follow(s)?",
         ["Only I", "Only II", "Both", "Neither"], 0,
         "I follows: some students are athletes and all athletes are fit, so some students are fit. II does not follow: nothing is said about students who are not athletes. Key Learning Point: “Some A are B” + “All B are C” gives only “Some A are C,” never “All A are C.”", "MEDIUM"),
        # Q13
        ("Painter : Canvas :: Writer : ?",
         ["Pen", "Paper", "Ink", "Novel"], 1,
         "A painter paints on a canvas; a writer writes on paper (the surface worked on). Novel is what a writer creates, and Pen and Ink are tools, so they show different relationships. Key Learning Point: Decide exactly which relationship the first pair shows (here, “surface worked on”) and reject options that show a different relationship.", "EASY"),
        # Q14
        ("Find the odd one out: Delhi, Mumbai, Bangalore, Ganges.",
         ["Delhi", "Mumbai", "Bangalore", "Ganges"], 3,
         "Delhi, Mumbai, and Bangalore are cities; the Ganges is a river. Key Learning Point: Check the category of every item – three are places of one kind and one belongs to a different category.", "EASY"),
        # Q15
        ("Find the next term: Y, W, T, P, ?",
         ["J", "K", "L", "M"], 1,
         "Gaps: Y→W (−2), W→T (−3), T→P (−4). The next gap is −5: P − 5 = K. Key Learning Point: When the gap changes steadily, continue the gap pattern to find the next letter.", "EASY"),
        # Q16
        ("Find the missing term: A1, C3, E5, G7, ?",
         ["H8", "I9", "I8", "J10"], 1,
         "Letters: A, C, E, G, I (+2 each). Numbers: 1, 3, 5, 7, 9 – each number is the position of its letter in the alphabet. Key Learning Point: In letter–number series, check the letter pattern and the number pattern separately, then see whether the two are linked.", "EASY"),
        # Q17
        ("Six people A, B, C, D, E, F sit in a row. D is 3rd from the left. F is immediately right of D. A is at the extreme right. E is immediately left of A. B is at the extreme left. Find C’s position.",
         ["1st", "2nd", "3rd", "5th"], 1,
         "B = 1st (extreme left), A = 6th (extreme right), E = 5th (immediately left of A). D = 3rd and F = 4th (immediately right of D). The only remaining position is 2nd, so C is 2nd. Key Learning Point: Fix the extreme positions first, then place the pairs linked by “immediately left/right”; the last person takes the remaining place.", "MEDIUM"),
        # Q18
        ("In a class of 45 students, Ravi ranks 18th from the bottom. Find his rank from the top.",
         ["26", "27", "28", "29"], 2,
         "Rank from top = Total − rank from bottom + 1 = 45 − 18 + 1 = 28. Key Learning Point: Rank from one end = Total − rank from the other end + 1.", "EASY"),
        # Q19
        ("In a row of 20 students, a boy is 7th from the right. Find his position from the left.",
         ["13", "14", "15", "16"], 1,
         "Position from left = 20 − 7 + 1 = 14. Key Learning Point: Position from the other end = Total − position from this end + 1.", "EASY"),
        # Q20
        ("If APPLE is coded as CRRNG, code GRAPE using the same pattern.",
         ["ITCRG", "ITCRH", "ITBRG", "JTCRG"], 0,
         "Verify pattern: A→C, P→R, P→R, L→N, E→G – each letter shifts forward by 2. GRAPE: G→I, R→T, A→C, P→R, E→G = ITCRG. Key Learning Point: Confirm the shift with every letter of the example, then apply it letter by letter.", "EASY"),
        # Q21
        ("A man says, “Her mother is the only daughter of my mother.” How is the man related to the woman referred to?",
         ["Uncle", "Father", "Brother", "Grandfather"], 0,
         "The only daughter of the man’s mother is the man’s sister. This sister is the woman’s mother, so the man is her mother’s brother – her uncle. Key Learning Point: Resolve the “only daughter of my mother” clue first; it usually points to the speaker or the speaker’s sibling.", "EASY"),
        # Q22
        ("At 3 o’clock, the minute hand of a clock points East. In which direction does the hour hand point?",
         ["North", "South", "East", "West"], 1,
         "At 3:00, the minute hand is at 12 and the hour hand is at 3, which is 90° clockwise from 12. 12 points East, so 90° clockwise from East = South. Key Learning Point: Convert clock positions into angles (each hour mark = 30°), then apply the turn to the given reference direction.", "MEDIUM"),
        # Q23
        ("Statements: No birds are mammals. All mammals are warm-blooded. Conclusion: No birds are warm-blooded. Does the conclusion follow?",
         ["Follows", "Does not follow", "Cannot be determined", "Both follow"], 1,
         "“No birds are mammals” + “All mammals are warm-blooded” does not give “No birds are warm-blooded” – birds may be warm-blooded without being mammals. Key Learning Point: A negative first premise with an “All” second premise cannot give a negative conclusion about the first and last terms.", "MEDIUM"),
        # Q24
        ("3 : 28 :: 4 : ?",
         ["63", "64", "65", "81"], 2,
         "3³ + 1 = 27 + 1 = 28, so the rule is “cube plus 1.” 4³ + 1 = 64 + 1 = 65. Key Learning Point: Test more than one operation (square, cube, ±1) on the first pair; the correct rule must give the second number exactly.", "EASY"),
        # Q25
        ("Four friends P, Q, R, and S sit around a square table, facing the centre. P sits opposite R, and Q sits to the immediate right of P. Who sits to the immediate left of P?",
         ["Q", "R", "S", "Cannot be determined"], 2,
         "P and R sit opposite each other, so P’s two neighbours are Q and S. Q is on P’s immediate right, so S must be on P’s immediate left. Key Learning Point: In arrangements around a table, fix one person first; the person opposite is never a neighbour, which narrows down the remaining places.", "MEDIUM"),
        # Q26
        ("Point Q is 4 km East of point P. Point R is 4 km North of Q. Point S is 4 km West of R. How far is S from P, and in which direction?",
         ["4 km North", "4 km East", "4√2 km North-East", "8 km North"], 0,
         "East 4 km and West 4 km cancel out. Only the 4 km North movement remains, so S is 4 km North of P. Key Learning Point: Trace the path as a sketch; when a route forms three sides of a square, the start and end points are one side apart.", "MEDIUM"),
        # Q27
        ("A’s mother is B. B’s brother is C. C’s daughter is D. How is D related to A?",
         ["Cousin", "Sister", "Aunt", "Niece"], 0,
         "B (A’s mother) and C are siblings, so C is A’s maternal uncle. C’s daughter D is therefore A’s cousin. Key Learning Point: A parent’s sibling’s child is always a cousin.", "MEDIUM"),
        # Q28
        ("Statements: All roses are flowers. Some flowers fade quickly. Conclusion: Some roses fade quickly. Does the conclusion follow?",
         ["Follows", "Does not follow", "Cannot be determined", "Both follow"], 1,
         "“All roses are flowers” + “Some flowers fade quickly” does not guarantee that any rose is among the flowers that fade quickly. Key Learning Point: “All A are B” + “Some B are C” does not give a definite conclusion about A and C.", "MEDIUM"),
        # Q29
        ("Find the missing term: ACE, CEG, EGI, ?",
         ["GIK", "GHK", "GIJ", "HIK"], 0,
         "Each group has three letters with a gap of 2 (A, C, E). First letters: A, C, E, G (+2), so the next group is G, I, K. Key Learning Point: Split a letter-group series into the starting-letter pattern and the within-group pattern.", "EASY"),
        # Q30
        ("In a row, Arun is 7th from the left and Bala is 12th from the right. When they interchange their positions, Arun becomes 15th from the left. How many people are in the row?",
         ["24", "25", "26", "27"], 2,
         "After interchanging, Arun takes Bala’s old place, so Bala’s place is 15th from the left. Bala’s place is also 12th from the right. Total = 15 + 12 − 1 = 26. Key Learning Point: In interchange questions, the new position of one person is the old position of the other – use it to get both ends of the same place.", "MEDIUM")
    ]

    # 30 Assessment Questions (Tamil)
    assess_ta = [
        # Q1
        ("GARDEN என்பது NEDRAG என எழுதப்பட்டால், அதே குறியீட்டில் FLOWER எவ்வாறு எழுதப்படும்?",
         ["REWOLF", "REWOFL", "RWEOLF", "FLOWRE"], 0,
         "GARDEN-ஐப் பின்னிருந்து எழுதினால் NEDRAG – இக்குறியீடு எழுத்துகளின் வரிசையை மட்டும் தலைகீழாக்குகிறது. FLOWER தலைகீழாக = REWOLF. முக்கியக் கற்றல் கருத்து: எல்லாக் குறியீடுகளும் எழுத்து நகர்வுகள் அல்ல – நகர்வைத் தேடும் முன், எழுத்துகள் மறுவரிசைப்படுத்தப்பட்டுள்ளனவா (இங்கு, தலைகீழாக்கப்பட்டுள்ளனவா) எனச் சரிபார்க்கவும்."),
        # Q2
        ("ஒரு சிறுமியைச் சுட்டிக்காட்டி ஒருவர், “இவள் என் மகனின் மகள்” என்கிறார். அவள் அவருக்கு என்ன உறவு?",
         ["மகள்", "பேத்தி", "மருமகள் (உடன்பிறந்தவரின் மகள்)", "சகோதரி"], 1,
         "அவரது மகனின் மகள், அவரது மகனின் பிள்ளை – மகனுக்கு ஒரு தலைமுறை கீழே உள்ளவள். எனவே அவள் அவருடைய பேத்தி. முக்கியக் கற்றல் கருத்து: மகன் அல்லது மகளின் பிள்ளை எப்போதும் பேரப்பிள்ளை – இருவருக்கும் இடையிலான தலைமுறைகளை எண்ணவும்."),
        # Q3
        ("சூரிய உதயத்தின்போது குமார் தன் நிழலை நோக்கி நிற்கிறார். அவர் எத்திசையை நோக்கியுள்ளார்?",
         ["வடக்கு", "தெற்கு", "கிழக்கு", "மேற்கு"], 3,
         "சூரிய உதயத்தின்போது சூரியன் கிழக்கில் உள்ளது; எனவே நிழல்கள் மேற்கு நோக்கி விழுகின்றன. தன் நிழலை நோக்கியிருப்பதால், குமார் மேற்கை நோக்கியுள்ளார். முக்கியக் கற்றல் கருத்து: நிழல் வினாக்களில், முதலில் சூரியனின் நிலையை (காலையில் கிழக்கு, மாலையில் மேற்கு) நிலைநிறுத்தவும்; நிழல் எப்போதும் எதிர்ப்புறத்தில் விழும்."),
        # Q4
        ("பசு : கன்று :: நாய் : ?",
         ["பூனைக்குட்டி", "நாய்க்குட்டி", "சிங்கக்குட்டி", "குதிரைக்குட்டி"], 1,
         "கன்று பசுவின் குட்டி; நாய்க்குட்டி நாயின் குட்டி. முக்கியக் கற்றல் கருத்து: பெரியது–குட்டி ஒப்புமைகள் ஒரு விலங்கை அதன் குட்டியின் குறிப்பிட்ட பெயருடன் இணைக்கின்றன; இரண்டாம் இணையும் அதே தொடர்பைக் காட்டுகிறதா எனச் சரிபார்க்கவும்."),
        # Q5
        ("பொருந்தாததைக் கண்டறிக: பசு, ஆடு, செம்மறியாடு, புலி.",
         ["பசு", "ஆடு", "செம்மறியாடு", "புலி"], 3,
         "பசு, ஆடு, செம்மறியாடு ஆகியவை தாவர உண்ணும் வீட்டு விலங்குகள்; புலி ஒரு ஊனுண்ணும் காட்டு விலங்கு. முக்கியக் கற்றல் கருத்து: பொருந்தாததைத் தனிப்படுத்த, பெரும்பாலான உருப்படிகளுக்குப் பொதுவான பண்பைத் (வீட்டு விலங்கு, தாவர உண்ணி) தேடவும்."),
        # Q6
        ("அடுத்த உறுப்பைக் காண்க: D, F, H, J, ?",
         ["K", "L", "M", "N"], 1,
         "அமைப்பு: ஒவ்வொரு முறையும் ஓர் எழுத்தைத் தவிர்க்கவும் (+2): D, F, H, J. J + 2 = L. முக்கியக் கற்றல் கருத்து: எழுத்துகளுக்கிடையிலான மாறா இடைவெளியை முதலில் சரிபார்க்கவும்; அதுவே எளிய எழுத்துத் தொடர் அமைப்பு."),
        # Q7
        ("A = 1, B = 2, C = 3, … Z = 26 மற்றும் CAT = 24 எனில், DOG = ?",
         ["24", "25", "26", "27"], 2,
         "CAT கொண்டு சரிபார்க்க: C(3) + A(1) + T(20) = 24; எனவே குறியீடு என்பது எழுத்துகளின் இட எண்களின் கூடுதல். DOG: D(4) + O(15) + G(7) = 26. முக்கியக் கற்றல் கருத்து: எழுத்து–எண் குறியீடுகளில், பயன்படுத்தும் முன் கொடுக்கப்பட்ட எடுத்துக்காட்டைக் கொண்டு விதியை (கூடுதல், பெருக்கல், அல்லது தலைகீழ் இடம்) உறுதிசெய்யவும்."),
        # Q8
        ("A என்பவர் B-இன் சகோதரி. C என்பவர் B-இன் தாய். D என்பவர் C-இன் தந்தை. A என்பவர் D-க்கு என்ன உறவு?",
         ["பேத்தி", "மகள்", "மருமகள் (உடன்பிறந்தவரின் மகள்)", "பேரன்"], 0,
         "C, B-இன் தாய்; A, B-இன் சகோதரி; எனவே C, A-க்கும் தாய். D, C-இன் தந்தை; எனவே D, A-இன் தாய்வழித் தாத்தா. A ஒரு பெண் (சகோதரி); எனவே A என்பவர் D-இன் பேத்தி. முக்கியக் கற்றல் கருத்து: வினாவின் திசையைக் கவனமாகப் படிக்கவும் – “A என்பவர் D-க்கு என்ன உறவு?” என்பதற்கு A-இன் பக்கத்திலிருந்து, A-இன் பாலினத்தைக் கொண்டு விடையளிக்க வேண்டும்."),
        # Q9
        ("ஒருவர் 5 கி.மீ வடக்கே, பின்னர் 3 கி.மீ கிழக்கே, பின்னர் 9 கி.மீ தெற்கே நடக்கிறார். அவர் தொடக்கப் புள்ளியிலிருந்து எவ்வளவு தூரத்தில், எத்திசையில் உள்ளார்?",
         ["5 கி.மீ தென்கிழக்கு", "5 கி.மீ வடகிழக்கு", "7 கி.மீ தென்கிழக்கு", "4 கி.மீ தெற்கு"], 0,
         "வடக்கு–தெற்கு: 5 கி.மீ வடக்கும் 9 கி.மீ தெற்கும் நிகராக 4 கி.மீ தெற்கைத் தருகின்றன. கிழக்கு–மேற்கு: 3 கி.மீ கிழக்கு. தூரம் = √(4² + 3²) = √25 = 5 கி.மீ, தென்கிழக்குத் திசையில். முக்கியக் கற்றல் கருத்து: முதலில் எதிர்த்திசை நகர்வுகளை நீக்கி, மீதமுள்ள செங்குத்துப் பகுதிகளைப் பிதாகரஸ் தொடர்பால் இணைக்கவும்; திசை அவ்விரு பகுதிகளிலிருந்து கிடைக்கிறது."),
        # Q10
        ("தென்கிழக்கு வடக்காக மாறினால், மேற்கு எதுவாக மாறும்?",
         ["வடகிழக்கு", "தென்கிழக்கு", "வடமேற்கு", "தெற்கு"], 1,
         "தென்கிழக்கிலிருந்து வடக்கு என்பது 135° எதிர்க்கடிகாரத் திருப்பம். மேற்கை 135° எதிர்க்கடிகாரச் சுற்றில் திருப்பினால்: மேற்கு → தென்மேற்கு → தெற்கு → தென்கிழக்கு. முக்கியக் கற்றல் கருத்து: திசைச் சுழற்சி வினாக்களில், கொடுக்கப்பட்ட இணையிலிருந்து திருப்பத்தின் கோணத்தையும் சுற்றுத் திசையையும் கண்டறிந்து, அதே திருப்பத்தைப் புதிய திசைக்குப் பயன்படுத்தவும்."),
        # Q11
        ("கூற்றுகள்: எல்லா மாம்பழங்களும் பழங்கள். எல்லாப் பழங்களும் ஆரோக்கியமானவை. முடிவு: எல்லா மாம்பழங்களும் ஆரோக்கியமானவை. முடிவு பொருந்துமா?",
         ["பொருந்துகிறது", "பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டும் பொருந்துகின்றன"], 0,
         "எல்லா மாம்பழங்களும் பழங்கள், எல்லாப் பழங்களும் ஆரோக்கியமானவை; எனவே எல்லா மாம்பழங்களும் ஆரோக்கியமானவை (எல்லா A-யும் B + எல்லா B-யும் C → எல்லா A-யும் C). முக்கியக் கற்றல் கருத்து: இரண்டு “எல்லா” கூற்றுகளின் சங்கிலி எப்போதும் செல்லத்தக்க “எல்லா” முடிவைத் தரும்."),
        # Q12
        ("கூற்றுகள்: சில மாணவர்கள் விளையாட்டு வீரர்கள். எல்லா விளையாட்டு வீரர்களும் உடல்தகுதி உடையவர்கள். முடிவுகள்: I. சில மாணவர்கள் உடல்தகுதி உடையவர்கள். II. எல்லா மாணவர்களும் உடல்தகுதி உடையவர்கள். எது/எவை பொருந்தும்?",
         ["I மட்டும்", "II மட்டும்", "இரண்டும்", "எதுவுமில்லை"], 0,
         "I பொருந்துகிறது: சில மாணவர்கள் விளையாட்டு வீரர்கள், எல்லா விளையாட்டு வீரர்களும் உடல்தகுதி உடையவர்கள்; எனவே சில மாணவர்கள் உடல்தகுதி உடையவர்கள். II பொருந்தவில்லை: விளையாட்டு வீரர்கள் அல்லாத மாணவர்கள் பற்றி எதுவும் கூறப்படவில்லை. முக்கியக் கற்றல் கருத்து: “சில A, B” + “எல்லா B-யும் C” என்பது “சில A, C” என்பதை மட்டுமே தரும்; ஒருபோதும் “எல்லா A-யும் C” எனத் தராது."),
        # Q13
        ("ஓவியர் : ஓவியத்திரை (கித்தான்) :: எழுத்தாளர் : ?",
         ["பேனா", "காகிதம்", "மை", "நாவல்"], 1,
         "ஓவியர் ஓவியத் திரையில் வரைகிறார்; எழுத்தாளர் காகிதத்தில் எழுதுகிறார் (பணிபுரியும் மேற்பரப்பு). நாவல் என்பது எழுத்தாளர் உருவாக்குவது; பேனாவும் மையும் கருவிகள் – எனவே அவை வேறு தொடர்புகளைக் காட்டுகின்றன. முக்கியக் கற்றல் கருத்து: முதல் இணை காட்டும் தொடர்பைத் (இங்கு, “பணிபுரியும் மேற்பரப்பு”) துல்லியமாக முடிவு செய்து, வேறு தொடர்பைக் காட்டும் விடைகளை நிராகரிக்கவும்."),
        # Q14
        ("பொருந்தாததைக் கண்டறிக: டெல்லி, மும்பை, பெங்களூரு, கங்கை.",
         ["டெல்லி", "மும்பை", "பெங்களூரு", "கங்கை"], 3,
         "டெல்லி, மும்பை, பெங்களூரு ஆகியவை நகரங்கள்; கங்கை ஒரு நதி. முக்கியக் கற்றல் கருத்து: ஒவ்வோர் உருப்படியின் வகைமையையும் சரிபார்க்கவும் – மூன்று ஒரே வகை இடங்கள்; ஒன்று வேறு வகையைச் சேர்ந்தது."),
        # Q15
        ("அடுத்த உறுப்பைக் காண்க: Y, W, T, P, ?",
         ["J", "K", "L", "M"], 1,
         "இடைவெளிகள்: Y→W (−2), W→T (−3), T→P (−4). அடுத்த இடைவெளி −5: P − 5 = K. முக்கியக் கற்றல் கருத்து: இடைவெளி சீராக மாறும்போது, அடுத்த எழுத்தைக் காண இடைவெளி அமைப்பைத் தொடரவும்."),
        # Q16
        ("விடுபட்ட உறுப்பைக் காண்க: A1, C3, E5, G7, ?",
         ["H8", "I9", "I8", "J10"], 1,
         "எழுத்துகள்: A, C, E, G, I (ஒவ்வொன்றும் +2). எண்கள்: 1, 3, 5, 7, 9 – ஒவ்வோர் எண்ணும் அதன் எழுத்தின் அகரவரிசை இட எண். முக்கியக் கற்றல் கருத்து: எழுத்து–எண் தொடர்களில், எழுத்து அமைப்பையும் எண் அமைப்பையும் தனித்தனியாகச் சரிபார்த்து, பின்னர் இரண்டும் தொடர்புடையவையா எனப் பார்க்கவும்."),
        # Q17
        ("A, B, C, D, E, F என்ற ஆறு பேர் ஒரு வரிசையில் அமர்ந்துள்ளனர். D இடமிருந்து 3-ஆவது இடத்தில் உள்ளார். F, D-க்கு உடனடியாக வலப்புறம் உள்ளார். A வலது ஓரத்தில் உள்ளார். E, A-க்கு உடனடியாக இடப்புறம் உள்ளார். B இடது ஓரத்தில் உள்ளார். C-இன் இடத்தைக் காண்க.",
         ["1-ஆவது", "2-ஆவது", "3-ஆவது", "5-ஆவது"], 1,
         "B = 1-ஆவது (இடது ஓரம்), A = 6-ஆவது (வலது ஓரம்), E = 5-ஆவது (A-க்கு உடனடியாக இடப்புறம்). D = 3-ஆவது, F = 4-ஆவது (D-க்கு உடனடியாக வலப்புறம்). மீதமுள்ள ஒரே இடம் 2-ஆவது; எனவே C 2-ஆவது இடத்தில் உள்ளார். முக்கியக் கற்றல் கருத்து: முதலில் ஓர இடங்களை நிலைநிறுத்தி, பின்னர் “உடனடியாக இடம்/வலம்” என இணைக்கப்பட்டவர்களை அமர்த்தவும்; கடைசி நபர் மீதமுள்ள இடத்தைப் பெறுவார்."),
        # Q18
        ("45 மாணவர்கள் கொண்ட ஒரு வகுப்பில், ரவி கீழிருந்து 18-ஆவது தரவரிசையில் உள்ளார். மேலிருந்து அவரது தரவரிசையைக் காண்க.",
         ["26", "27", "28", "29"], 2,
         "மேலிருந்து தரவரிசை = மொத்தம் − கீழிருந்து தரவரிசை + 1 = 45 − 18 + 1 = 28. முக்கியக் கற்றல் கருத்து: ஒரு முனையிலிருந்து தரவரிசை = மொத்தம் − மறுமுனையிலிருந்து தரவரிசை + 1."),
        # Q19
        ("20 மாணவர்கள் கொண்ட ஒரு வரிசையில், ஒரு சிறுவன் வலமிருந்து 7-ஆவதாக உள்ளான். இடமிருந்து அவனது இடத்தைக் காண்க.",
         ["13", "14", "15", "16"], 1,
         "இடமிருந்து இடம் = 20 − 7 + 1 = 14. முக்கியக் கற்றல் கருத்து: மறுமுனையிலிருந்து இடம் = மொத்தம் − இம்முனையிலிருந்து இடம் + 1."),
        # Q20
        ("APPLE என்பது CRRNG எனக் குறியிடப்பட்டால், அதே அமைப்பில் GRAPE-ஐக் குறியிடுக.",
         ["ITCRG", "ITCRH", "ITBRG", "JTCRG"], 0,
         "அமைப்பைச் சரிபார்க்க: A→C, P→R, P→R, L→N, E→G – ஒவ்வோர் எழுத்தும் 2 இடங்கள் முன்னோக்கி நகர்கிறது. GRAPE: G→I, R→T, A→C, P→R, E→G = ITCRG. முக்கியக் கற்றல் கருத்து: எடுத்துக்காட்டின் ஒவ்வோர் எழுத்தையும் கொண்டு நகர்வை உறுதிசெய்து, பின்னர் ஒவ்வோர் எழுத்தாகப் பயன்படுத்தவும்."),
        # Q21
        ("ஒருவர், “அவளுடைய தாய் என் தாயின் ஒரே மகள்” என்கிறார். குறிப்பிடப்பட்ட பெண்ணுக்கு அவர் என்ன உறவு?",
         ["தாய்மாமா (தாயின் சகோதரர்)", "தந்தை", "சகோதரர்", "தாத்தா"], 0,
         "அவரது தாயின் ஒரே மகள் அவருடைய சகோதரி. இச்சகோதரியே அப்பெண்ணின் தாய்; எனவே அவர் அப்பெண்ணின் தாயின் சகோதரர் – அவளுடைய தாய்மாமா. முக்கியக் கற்றல் கருத்து: “என் தாயின் ஒரே மகள்” என்ற குறிப்பை முதலில் தீர்க்கவும்; அது பொதுவாகப் பேசுபவரையோ அவரது உடன்பிறந்தவரையோ குறிக்கிறது."),
        # Q22
        ("மணி 3 ஆகும்போது, ஒரு கடிகாரத்தின் நிமிட முள் கிழக்கைக் காட்டுகிறது. மணி முள் எத்திசையைக் காட்டும்?",
         ["வடக்கு", "தெற்கு", "கிழக்கு", "மேற்கு"], 1,
         "3:00 மணிக்கு நிமிட முள் 12-இலும் மணி முள் 3-இலும் உள்ளன; 3 என்பது 12-இலிருந்து 90° கடிகாரச் சுற்றில் உள்ளது. 12 கிழக்கைக் காட்டுகிறது; எனவே கிழக்கிலிருந்து 90° கடிகாரச் சுற்று = தெற்கு. முக்கியக் கற்றல் கருத்து: கடிகார நிலைகளைக் கோணங்களாக மாற்றி (ஒவ்வொரு மணிக் குறியும் = 30°), பின்னர் அத்திருப்பத்தைக் கொடுக்கப்பட்ட குறிப்புத் திசைக்குப் பயன்படுத்தவும்."),
        # Q23
        ("கூற்றுகள்: எந்தப் பறவையும் பாலூட்டி அல்ல. எல்லாப் பாலூட்டிகளும் வெப்ப இரத்தப் பிராணிகள். முடிவு: எந்தப் பறவையும் வெப்ப இரத்தப் பிராணி அல்ல. முடிவு பொருந்துமா?",
         ["பொருந்துகிறது", "பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டும் பொருந்துகின்றன"], 1,
         "“எந்தப் பறவையும் பாலூட்டி அல்ல” + “எல்லாப் பாலூட்டிகளும் வெப்ப இரத்தப் பிராணிகள்” என்பது “எந்தப் பறவையும் வெப்ப இரத்தப் பிராணி அல்ல” எனத் தராது – பறவைகள் பாலூட்டிகளாக இல்லாமலேயே வெப்ப இரத்தப் பிராணிகளாக இருக்கலாம். முக்கியக் கற்றல் கருத்து: முதல் கூற்று எதிர்மறையாகவும் இரண்டாம் கூற்று “எல்லா” எனவும் இருந்தால், முதல் மற்றும் கடைசிச் சொற்கள் குறித்து எதிர்மறை முடிவைத் தர இயலாது."),
        # Q24
        ("3 : 28 :: 4 : ?",
         ["63", "64", "65", "81"], 2,
         "3³ + 1 = 27 + 1 = 28; எனவே விதி “கனம் கூட்டல் 1.” 4³ + 1 = 64 + 1 = 65. முக்கியக் கற்றல் கருத்து: முதல் இணையில் ஒன்றுக்கு மேற்பட்ட செயல்களை (வர்க்கம், கனம், ±1) சோதிக்கவும்; சரியான விதி இரண்டாம் எண்ணைத் துல்லியமாகத் தர வேண்டும்."),
        # Q25
        ("P, Q, R, S என்ற நான்கு நண்பர்கள் ஒரு சதுர மேசையைச் சுற்றி, மையத்தை நோக்கி அமர்ந்துள்ளனர். P, R-க்கு எதிரே அமர்ந்துள்ளார்; Q, P-க்கு உடனடியாக வலப்புறம் அமர்ந்துள்ளார். P-க்கு உடனடியாக இடப்புறம் அமர்ந்திருப்பவர் யார்?",
         ["Q", "R", "S", "தீர்மானிக்க இயலாது"], 2,
         "P-யும் R-உம் ஒருவருக்கொருவர் எதிரே அமர்ந்துள்ளனர்; எனவே P-இன் இரு அண்டையர் Q-உம் S-உம். Q, P-க்கு உடனடியாக வலப்புறம் உள்ளார்; எனவே S, P-க்கு உடனடியாக இடப்புறம் இருக்க வேண்டும். முக்கியக் கற்றல் கருத்து: மேசையைச் சுற்றிய அமைப்புகளில், முதலில் ஒருவரை நிலைநிறுத்தவும்; எதிரே அமர்ந்திருப்பவர் ஒருபோதும் அண்டையர் அல்ல – இது மீதமுள்ள இடங்களைக் குறுக்குகிறது."),
        # Q26
        ("புள்ளி Q, புள்ளி P-க்கு 4 கி.மீ கிழக்கே உள்ளது. புள்ளி R, Q-க்கு 4 கி.மீ வடக்கே உள்ளது. புள்ளி S, R-க்கு 4 கி.மீ மேற்கே உள்ளது. S, P-இலிருந்து எவ்வளவு தூரத்தில், எத்திசையில் உள்ளது?",
         ["4 கி.மீ வடக்கு", "4 கி.மீ கிழக்கு", "4√2 கி.மீ வடகிழக்கு", "8 கி.மீ வடக்கு"], 0,
         "கிழக்கு 4 கி.மீ-உம் மேற்கு 4 கி.மீ-உம் ஒன்றையொன்று நீக்குகின்றன. 4 கி.மீ வடக்கு நகர்வு மட்டுமே மீதமுள்ளது; எனவே S, P-க்கு 4 கி.மீ வடக்கே உள்ளது. முக்கியக் கற்றல் கருத்து: பாதையை ஒரு வரைபடமாக வரையவும்; ஒரு பாதை சதுரத்தின் மூன்று பக்கங்களை அமைக்கும்போது, தொடக்கமும் முடிவும் ஒரு பக்க தூரத்தில் இருக்கும்."),
        # Q27
        ("A-இன் தாய் B. B-இன் சகோதரர் C. C-இன் மகள் D. D என்பவர் A-க்கு என்ன உறவு?",
         ["ஒன்றுவிட்ட உடன்பிறப்பு (Cousin)", "சகோதரி", "அத்தை", "மருமகள் (உடன்பிறந்தவரின் மகள்)"], 0,
         "B (A-இன் தாய்) மற்றும் C உடன்பிறந்தவர்கள்; எனவே C, A-இன் தாய்மாமா. எனவே C-இன் மகள் D, A-இன் ஒன்றுவிட்ட உடன்பிறப்பு (Cousin). முக்கியக் கற்றல் கருத்து: பெற்றோரின் உடன்பிறந்தவரின் பிள்ளை எப்போதும் ஒன்றுவிட்ட உடன்பிறப்பு (Cousin) ஆவார்."),
        # Q28
        ("கூற்றுகள்: எல்லா ரோஜாக்களும் பூக்கள். சில பூக்கள் விரைவில் வாடுகின்றன. முடிவு: சில ரோஜாக்கள் விரைவில் வாடுகின்றன. முடிவு பொருந்துமா?",
         ["பொருந்துகிறது", "பொருந்தவில்லை", "தீர்மானிக்க இயலாது", "இரண்டும் பொருந்துகின்றன"], 1,
         "“எல்லா ரோஜாக்களும் பூக்கள்” + “சில பூக்கள் விரைவில் வாடுகின்றன” என்பது, விரைவில் வாடும் பூக்களில் ஏதேனும் ரோஜா இருப்பதை உறுதிசெய்யாது. முக்கியக் கற்றல் கருத்து: “எல்லா A-யும் B” + “சில B, C” என்பது A மற்றும் C குறித்து உறுதியான முடிவைத் தராது."),
        # Q29
        ("விடுபட்ட உறுப்பைக் காண்க: ACE, CEG, EGI, ?",
         ["GIK", "GHK", "GIJ", "HIK"], 0,
         "ஒவ்வொரு குழுவிலும் 2 இடைவெளியுடன் மூன்று எழுத்துகள் உள்ளன (A, C, E). முதல் எழுத்துகள்: A, C, E, G (+2); எனவே அடுத்த குழு G, I, K. முக்கியக் கற்றல் கருத்து: எழுத்துக் குழுத் தொடரைத் தொடக்க எழுத்து அமைப்பு மற்றும் குழுவுக்குள் உள்ள அமைப்பு எனப் பிரிக்கவும்."),
        # Q30
        ("ஒரு வரிசையில் அருண் இடமிருந்து 7-ஆவதாகவும் பாலா வலமிருந்து 12-ஆவதாகவும் உள்ளனர். அவர்கள் தங்கள் இடங்களை மாற்றிக்கொண்டால், அருண் இடமிருந்து 15-ஆவதாக ஆகிறார். வரிசையில் எத்தனை பேர் உள்ளனர்?",
         ["24", "25", "26", "27"], 2,
         "இடம் மாறிய பின் அருண் பாலாவின் பழைய இடத்தைப் பெறுகிறார்; எனவே பாலாவின் இடம் இடமிருந்து 15-ஆவது. பாலாவின் இடம் வலமிருந்து 12-ஆவதும் ஆகும். மொத்தம் = 15 + 12 − 1 = 26. முக்கியக் கற்றல் கருத்து: இடமாற்ற வினாக்களில், ஒருவரின் புதிய இடம் மற்றவரின் பழைய இடமாகும் – அதைக்கொண்டு அதே இடத்தின் இரு முனைகளையும் பெறவும்.")
    ]

    print(f"Worked: EN={len(worked_en)}, TA={len(worked_ta)}")
    print(f"Indep: EN={len(indep_en)}, TA={len(indep_ta)}")
    print(f"Assess: EN={len(assess_en)}, TA={len(assess_ta)}")

    # Combine Practice Set: 25 Worked + 30 Independent = 55 Questions
    prac_en = worked_en + indep_en
    prac_ta = worked_ta + indep_ta
    assert len(prac_en) == 55
    assert len(prac_ta) == 55
    assert len(assess_en) == 30
    assert len(assess_ta) == 30

    out_lines = []
    out_lines.append("/* ============================================================================")
    out_lines.append("   ExamPro LMS - Logical Reasoning Course Seed Script (Unified Bilingual Model)")
    out_lines.append("   - 1 Course: Logical Reasoning / தருக்கக் காரணவியல்")
    out_lines.append("   - 2 Assessments (Single unified assessment for both English & Tamil):")
    out_lines.append("       1. Logical Reasoning - Practice Set (logical-reasoning-practice) [55 Questions]")
    out_lines.append("          (25 Worked Examples + 30 Independent Practice in both English & Tamil)")
    out_lines.append("       2. Logical Reasoning - Graded Assessment (logical-reasoning-graded) [30 Questions]")
    out_lines.append("          (Assessment Questions 1-30 in both English & Tamil)")
    out_lines.append("   ============================================================================ */")
    out_lines.append("USE ExamProLMS;")
    out_lines.append("GO")
    out_lines.append("SET QUOTED_IDENTIFIER ON;")
    out_lines.append("GO")
    out_lines.append("")
    out_lines.append("-- Step 1: Ensure bilingual columns exist in dbo.Assessments & dbo.Questions")
    out_lines.append("IF COL_LENGTH(N'dbo.Assessments', N'TitleTa') IS NULL")
    out_lines.append("    ALTER TABLE dbo.Assessments ADD TitleTa NVARCHAR(200) NULL;")
    out_lines.append("IF COL_LENGTH(N'dbo.Assessments', N'DescriptionTa') IS NULL")
    out_lines.append("    ALTER TABLE dbo.Assessments ADD DescriptionTa NVARCHAR(MAX) NULL;")
    out_lines.append("IF COL_LENGTH(N'dbo.Questions', N'QuestionTextTa') IS NULL")
    out_lines.append("    ALTER TABLE dbo.Questions ADD QuestionTextTa NVARCHAR(MAX) NULL;")
    out_lines.append("IF COL_LENGTH(N'dbo.Questions', N'OptionsJsonTa') IS NULL")
    out_lines.append("    ALTER TABLE dbo.Questions ADD OptionsJsonTa NVARCHAR(MAX) NULL;")
    out_lines.append("IF COL_LENGTH(N'dbo.Questions', N'ExplanationTa') IS NULL")
    out_lines.append("    ALTER TABLE dbo.Questions ADD ExplanationTa NVARCHAR(MAX) NULL;")
    out_lines.append("GO")
    out_lines.append("")
    out_lines.append("BEGIN TRANSACTION;")
    out_lines.append("")
    out_lines.append("-- Clean previous Logical Reasoning courses and assessments if present")
    out_lines.append("DELETE FROM dbo.Assessments WHERE Slug IN (")
    out_lines.append("    N'logical-reasoning-practice', N'logical-reasoning-graded',")
    out_lines.append("    N'logical-reasoning-practice-en', N'logical-reasoning-graded-en',")
    out_lines.append("    N'logical-reasoning-practice-ta', N'logical-reasoning-graded-ta'")
    out_lines.append(");")
    out_lines.append("DELETE FROM dbo.Courses WHERE Slug IN (N'logical-reasoning');")
    out_lines.append("")
    out_lines.append("INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)")
    out_lines.append("VALUES (")
    out_lines.append("    N'Logical Reasoning / தருக்கக் காரணவியல்',")
    out_lines.append("    N'logical-reasoning',")
    out_lines.append("    N'Comprehensive module on Coding-Decoding, Blood Relations, Direction Sense, Syllogisms, Ranking, and Analogies for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',")
    out_lines.append("    5")
    out_lines.append(");")
    out_lines.append("")
    out_lines.append("DECLARE @CourseId INT = SCOPE_IDENTITY();")
    out_lines.append("")
    out_lines.append("-- Insert ONLY 2 Assessments: 1 Practice (55 Questions) and 1 Graded (30 Questions)")
    out_lines.append("INSERT INTO dbo.Assessments (")
    out_lines.append("    CourseId, Title, TitleTa, Slug, Description, DescriptionTa, Topic, Difficulty,")
    out_lines.append("    DefaultDurationMinutes, MinDurationMinutes, TotalQuestions, PassPercentage,")
    out_lines.append("    AttemptType, SequentialUnlock, LockdownEnabled, ProctoringEnabled, OrderIndex")
    out_lines.append(")")
    out_lines.append("VALUES")
    out_lines.append("    (@CourseId, N'Logical Reasoning - Practice Set', N'தருக்கக் காரணவியல் - பயிற்சித் தொகுப்பு', N'logical-reasoning-practice',")
    out_lines.append("     N'55 practice questions (Worked Examples + Independent Practice) with instant feedback & step-by-step solutions.',")
    out_lines.append("     N'55 பயிற்சிக் கணக்குகள் (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனடித் தீர்வுகளுடன்.',")
    out_lines.append("     N'Logical Reasoning', N'EASY', 60, 10, 55, 0, N'PRACTICE', 0, 0, 0, 1),")
    out_lines.append("    (@CourseId, N'Logical Reasoning - Graded Assessment', N'தருக்கக் காரணவியல் - மதிப்பீட்டுத் தேர்வு', N'logical-reasoning-graded',")
    out_lines.append("     N'Official proctored & timed assessment on Logical Reasoning (30 Questions). Pass with 60% to master this topic.',")
    out_lines.append("     N'தருக்கக் காரணவியலுக்கான அதிகாரப்பூர்வக் கண்காணிப்புடன் கூடிய தேர்வு (30 வினாக்கள்). தேர்ச்சி 60%.',")
    out_lines.append("     N'Logical Reasoning', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 2);")
    out_lines.append("")
    out_lines.append("DECLARE @pracId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'logical-reasoning-practice');")
    out_lines.append("DECLARE @gradId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'logical-reasoning-graded');")
    out_lines.append("")
    out_lines.append("-- Insert bilingual questions for @pracId (55 questions)")
    out_lines.append("INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, QuestionTextTa, OptionsJsonTa, ExplanationTa, Topic, Difficulty, OrderIndex)")
    out_lines.append("VALUES")

    p_rows = []
    for idx, (en, ta) in enumerate(zip(prac_en, prac_ta), start=1):
        q_en, opts_en, ans_en, exp_en, diff_en = en
        q_ta, opts_ta, ans_ta, exp_ta = ta
        p_rows.append(f"    (@pracId, {escape_sql(q_en)}, {escape_sql(json.dumps(opts_en, ensure_ascii=False))}, {ans_en}, {escape_sql(exp_en)}, {escape_sql(q_ta)}, {escape_sql(json.dumps(opts_ta, ensure_ascii=False))}, {escape_sql(exp_ta)}, N'Logical Reasoning', N'{diff_en}', {idx})")

    out_lines.append(",\n".join(p_rows) + ";")
    out_lines.append("")

    out_lines.append("-- Insert bilingual questions for @gradId (30 questions)")
    out_lines.append("INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, QuestionTextTa, OptionsJsonTa, ExplanationTa, Topic, Difficulty, OrderIndex)")
    out_lines.append("VALUES")

    g_rows = []
    for idx, (en, ta) in enumerate(zip(assess_en, assess_ta), start=1):
        q_en, opts_en, ans_en, exp_en, diff_en = en
        q_ta, opts_ta, ans_ta, exp_ta = ta
        g_rows.append(f"    (@gradId, {escape_sql(q_en)}, {escape_sql(json.dumps(opts_en, ensure_ascii=False))}, {ans_en}, {escape_sql(exp_en)}, {escape_sql(q_ta)}, {escape_sql(json.dumps(opts_ta, ensure_ascii=False))}, {escape_sql(exp_ta)}, N'Logical Reasoning', N'{diff_en}', {idx})")

    out_lines.append(",\n".join(g_rows) + ";")
    out_lines.append("")
    out_lines.append("COMMIT;")
    out_lines.append("PRINT 'Logical Reasoning Course seeded successfully: 1 Practice Assessment (55 Qs) and 1 Graded Assessment (30 Qs), fully bilingual (English & Tamil).';")
    out_lines.append("GO")

    out_path = os.path.join(os.path.dirname(__file__), "08_logical_reasoning_bilingual_seed.sql")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Generated {out_path} ({len(out_lines)} lines)")

if __name__ == '__main__':
    main()
