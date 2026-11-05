# -*- coding: utf-8 -*-
"""Generates 10_simplification_bilingual_seed.sql containing all 85 questions from English and Tamil Simplification PDFs."""
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
        ("Simplify: 15 + 6 × 3",
         ["33", "63", "27", "51"], 0,
         "By BODMAS, multiplication first: 6×3=18. Then 15+18 = 33. Key Learning Point: Multiplication is performed before addition, regardless of the order the operations are written in.", "EASY"),
        # Q2
        ("Simplify: (12 + 8) ÷ 4",
         ["4", "5", "6", "8"], 1,
         "Brackets first: 12+8=20. Then 20÷4 = 5. Key Learning Point: Always resolve brackets before any other operation.", "EASY"),
        # Q3
        ("Simplify: 3/4 + 1/4",
         ["1/2", "3/4", "1", "5/4"], 2,
         "Same denominator: 3/4+1/4 = 4/4 = 1. Key Learning Point: When denominators are already equal, simply add the numerators.", "EASY"),
        # Q4
        ("Simplify: 2³ × 2²",
         ["16", "32", "64", "2"], 1,
         "Same base, multiplication: add exponents. 2^(3+2) = 2^5 = 32. Key Learning Point: When multiplying powers with the same base, add the exponents.", "EASY"),
        # Q5
        ("Simplify: 0.5 + 0.25",
         ["0.65", "0.7", "0.75", "0.8"], 2,
         "0.5 + 0.25 = 0.75. Key Learning Point: Align decimal points carefully when adding decimal numbers.", "EASY"),
        # Q6
        ("Simplify: 18 ÷ 3 × 2 + 4 − 5",
         ["9", "10", "11", "12"], 2,
         "Division and multiplication, left to right: 18÷3=6, 6×2=12. Then addition/subtraction: 12+4=16, 16−5=11. Key Learning Point: When an expression has both division and multiplication with no brackets, perform them left to right in the order they appear.", "EASY"),
        # Q7
        ("Simplify: [16 − (8 ÷ 2)] × 3",
         ["30", "33", "36", "40"], 2,
         "Innermost bracket first: 8÷2=4. Then 16−4=12. Then 12×3 = 36. Key Learning Point: Resolve the innermost bracket first, then work outward.", "EASY"),
        # Q8
        ("Simplify: 2/3 + 3/4 − 1/6",
         ["1", "5/4", "4/3", "3/2"], 1,
         "LCM = 12: 8/12 + 9/12 − 2/12 = 15/12 = 5/4. Key Learning Point: Convert all fractions to a common denominator (LCM) before adding or subtracting.", "EASY"),
        # Q9
        ("Simplify: 0.75 × 0.4 + 0.15",
         ["0.35", "0.4", "0.45", "0.5"], 2,
         "0.75×0.4 = 0.3. Then 0.3+0.15 = 0.45. Key Learning Point: Complete multiplication of decimals before addition, following BODMAS.", "EASY"),
        # Q10
        ("Simplify: (5² − 3²) ÷ (5 − 3)",
         ["6", "7", "8", "9"], 2,
         "(25−9) ÷ 2 = 16÷2 = 8. Key Learning Point: Resolve each bracket fully before performing the operation between them.", "EASY"),
        # Q11
        ("Simplify: √144 + √81",
         ["19", "20", "21", "22"], 2,
         "√144=12, √81=9. 12+9 = 21. Key Learning Point: Memorising perfect squares speeds up square-root simplification significantly.", "EASY"),
        # Q12
        ("Simplify: 2⁴ × 2³ ÷ 2⁵",
         ["2", "4", "8", "16"], 1,
         "Same base: 2^(4+3−5) = 2^2 = 4. Key Learning Point: Combine all exponent operations on the same base into a single exponent before evaluating.", "EASY"),
        # Q13
        ("Simplify: (1/2 + 1/3) ÷ (1/2 − 1/3)",
         ["3", "4", "5", "6"], 2,
         "1/2+1/3 = 5/6. 1/2−1/3 = 1/6. (5/6) ÷ (1/6) = 5. Key Learning Point: Fully simplify each bracket to a single fraction before dividing one by the other.", "EASY"),
        # Q14
        ("Simplify: 3.6 ÷ 1.2 + 2.5 × 2",
         ["6", "7", "8", "9"], 2,
         "3.6÷1.2=3. 2.5×2=5. 3+5 = 8. Key Learning Point: Perform division and multiplication before addition, even with decimal numbers.", "EASY"),
        # Q15
        ("Simplify √50 into its simplest radical form.",
         ["2√5", "4√5", "5√2", "10√5"], 2,
         "50 = 25×2. √50 = √25×√2 = 5√2. Key Learning Point: To simplify a surd, factor out the largest perfect square from under the root.", "EASY"),
        # Q16
        ("Simplify: a²b³ × a³b²",
         ["a⁵b⁵", "a⁶b⁶", "a⁵b⁶", "a⁶b⁵"], 0,
         "Add exponents of like bases: a^(2+3) b^(3+2) = a⁵b⁵. Key Learning Point: When multiplying terms with multiple variable bases, add exponents for each base separately.", "EASY"),
        # Q17
        ("Simplify: 2 1/3 + 1 1/2",
         ["3 1/6", "3 5/6", "4 1/6", "4 5/6"], 1,
         "2 1/3 = 7/3, 1 1/2 = 3/2. LCM=6: 14/6 + 9/6 = 23/6 = 3 5/6. Key Learning Point: Convert mixed numbers to improper fractions before adding, then convert back at the end.", "EASY"),
        # Q18
        ("Express the recurring decimal 0.333… as a fraction.",
         ["1/2", "1/3", "1/4", "3/10"], 1,
         "0.333… = 1/3 (a standard recurring-decimal conversion). Key Learning Point: Common recurring decimals like 0.333… = 1/3 and 0.666… = 2/3 are worth memorising directly.", "EASY"),
        # Q19
        ("Simplify: 1 ÷ (1/2 + 1/3 + 1/6)",
         ["1/2", "1", "3/2", "2"], 1,
         "1/2+1/3+1/6 = 3/6+2/6+1/6 = 6/6 = 1. Then 1÷1 = 1. Key Learning Point: Resolve the bracket to a single value first before performing the outer operation.", "EASY"),
        # Q20
        ("Simplify the complex fraction: (2 + 1/3) ÷ (1 − 1/4)",
         ["7/3", "3/4", "28/9", "9/4"], 2,
         "2+1/3 = 7/3. 1−1/4 = 3/4. (7/3) ÷ (3/4) = 7/3 × 4/3 = 28/9. Key Learning Point: In a complex fraction, fully simplify the numerator and denominator separately before dividing.", "MEDIUM"),
        # Q21
        ("Simplify: 64^(1/2) − 27^(1/3)",
         ["3", "4", "5", "6"], 2,
         "64^(1/2) = 8 (square root). 27^(1/3) = 3 (cube root). 8−3 = 5. Key Learning Point: A fractional exponent of 1/2 means square root; 1/3 means cube root.", "EASY"),
        # Q22
        ("Simplify: 2.25 × 4 − 1.5²",
         ["5.75", "6.25", "6.75", "7.25"], 2,
         "2.25×4 = 9. 1.5² = 2.25. 9−2.25 = 6.75. Key Learning Point: Evaluate powers before subtraction, following BODMAS even with decimals.", "EASY"),
        # Q23
        ("Simplify: (3/5 of 25) + (2/7 of 49)",
         ["27", "28", "29", "30"], 2,
         "3/5 of 25 = 15. 2/7 of 49 = 14. 15+14 = 29. Key Learning Point: “Of” in fraction problems means multiplication – compute each “of” term separately before combining.", "EASY"),
        # Q24
        ("Find the approximate value of √99.8 (nearest whole number).",
         ["9", "10", "11", "12"], 1,
         "99.8 is very close to 100, and √100 = 10. Key Learning Point: For approximation, round the number to the nearest perfect square/cube first, then compute.", "EASY"),
        # Q25
        ("Simplify: [(3+2)² − (3−2)²] ÷ (3×2)",
         ["2", "3", "4", "5"], 2,
         "(5² − 1²) ÷ 6 = (25−1) ÷ 6 = 24÷6 = 4. Key Learning Point: This expression is an example of the identity (a+b)²−(a−b)² = 4ab, which always simplifies to exactly 4 when divided by ab – recognising such identities saves computation time.", "MEDIUM")
    ]

    # 25 Worked Examples (Tamil)
    worked_ta = [
        # Q1
        ("சுருக்குக: 15 + 6 × 3",
         ["33", "63", "27", "51"], 0,
         "BODMAS-இன்படி முதலில் பெருக்கல்: 6×3=18. பின்னர் 15+18 = 33. முக்கியக் கற்றல் கருத்து: செயல்கள் எழுதப்பட்ட வரிசை எதுவாக இருந்தாலும், கூட்டலுக்கு முன் பெருக்கல் செய்யப்படுகிறது."),
        # Q2
        ("சுருக்குக: (12 + 8) ÷ 4",
         ["4", "5", "6", "8"], 1,
         "முதலில் அடைப்புக்குறி: 12+8=20. பின்னர் 20÷4 = 5. முக்கியக் கற்றல் கருத்து: வேறு எந்தச் செயலுக்கும் முன் எப்போதும் அடைப்புக்குறிகளைத் தீர்க்கவும்."),
        # Q3
        ("சுருக்குக: 3/4 + 1/4",
         ["1/2", "3/4", "1", "5/4"], 2,
         "ஒரே பகுதி: 3/4+1/4 = 4/4 = 1. முக்கியக் கற்றல் கருத்து: பகுதிகள் ஏற்கெனவே சமமாக இருக்கும்போது, தொகுதிகளை மட்டும் கூட்டவும்."),
        # Q4
        ("சுருக்குக: 2³ × 2²",
         ["16", "32", "64", "2"], 1,
         "ஒரே அடிமானம், பெருக்கல்: அடுக்குகளைக் கூட்டவும். 2^(3+2) = 2^5 = 32. முக்கியக் கற்றல் கருத்து: ஒரே அடிமானம் கொண்ட அடுக்குகளைப் பெருக்கும்போது, அடுக்குகளைக் கூட்டவும்."),
        # Q5
        ("சுருக்குக: 0.5 + 0.25",
         ["0.65", "0.7", "0.75", "0.8"], 2,
         "0.5 + 0.25 = 0.75. முக்கியக் கற்றல் கருத்து: தசம எண்களைக் கூட்டும்போது தசமப் புள்ளிகளைக் கவனமாக நேராக்கவும்."),
        # Q6
        ("சுருக்குக: 18 ÷ 3 × 2 + 4 − 5",
         ["9", "10", "11", "12"], 2,
         "வகுத்தலும் பெருக்கலும், இடமிருந்து வலமாக: 18÷3=6, 6×2=12. பின்னர் கூட்டல்/கழித்தல்: 12+4=16, 16−5=11. முக்கியக் கற்றல் கருத்து: அடைப்புக்குறிகள் இல்லாத கோவையில் வகுத்தலும் பெருக்கலும் இருக்கும்போது, அவை தோன்றும் வரிசையில் இடமிருந்து வலமாகச் செய்யவும்."),
        # Q7
        ("சுருக்குக: [16 − (8 ÷ 2)] × 3",
         ["30", "33", "36", "40"], 2,
         "முதலில் உள்ளார்ந்த அடைப்புக்குறி: 8÷2=4. பின்னர் 16−4=12. பின்னர் 12×3 = 36. முக்கியக் கற்றல் கருத்து: முதலில் உள்ளார்ந்த அடைப்புக்குறியைத் தீர்த்து, பின்னர் வெளிநோக்கிச் செயல்படவும்."),
        # Q8
        ("சுருக்குக: 2/3 + 3/4 − 1/6",
         ["1", "5/4", "4/3", "3/2"], 1,
         "மீ.பொ.ம = 12: 8/12 + 9/12 − 2/12 = 15/12 = 5/4. முக்கியக் கற்றல் கருத்து: கூட்டும் அல்லது கழிக்கும் முன் அனைத்துப் பின்னங்களையும் பொதுப் பகுதிக்கு (மீ.பொ.ம) மாற்றவும்."),
        # Q9
        ("சுருக்குக: 0.75 × 0.4 + 0.15",
         ["0.35", "0.4", "0.45", "0.5"], 2,
         "0.75×0.4 = 0.3. பின்னர் 0.3+0.15 = 0.45. முக்கியக் கற்றல் கருத்து: BODMAS-இன்படி, கூட்டலுக்கு முன் தசமங்களின் பெருக்கலை முடிக்கவும்."),
        # Q10
        ("சுருக்குக: (5² − 3²) ÷ (5 − 3)",
         ["6", "7", "8", "9"], 2,
         "(25−9) ÷ 2 = 16÷2 = 8. முக்கியக் கற்றல் கருத்து: அடைப்புக்குறிகளுக்கு இடையிலான செயலைச் செய்யும் முன், ஒவ்வோர் அடைப்புக்குறியையும் முழுமையாகத் தீர்க்கவும்."),
        # Q11
        ("சுருக்குக: √144 + √81",
         ["19", "20", "21", "22"], 2,
         "√144=12, √81=9. 12+9 = 21. முக்கியக் கற்றல் கருத்து: முழு வர்க்கங்களை மனப்பாடம் செய்வது வர்க்கமூலச் சுருக்குதலைப் பெரிதும் விரைவுபடுத்துகிறது."),
        # Q12
        ("சுருக்குக: 2⁴ × 2³ ÷ 2⁵",
         ["2", "4", "8", "16"], 1,
         "ஒரே அடிமானம்: 2^(4+3−5) = 2^2 = 4. முக்கியக் கற்றல் கருத்து: மதிப்பிடும் முன், ஒரே அடிமானத்தின் மீதான அனைத்து அடுக்குச் செயல்களையும் ஒரே அடுக்காக இணைக்கவும்."),
        # Q13
        ("சுருக்குக: (1/2 + 1/3) ÷ (1/2 − 1/3)",
         ["3", "4", "5", "6"], 2,
         "1/2+1/3 = 5/6. 1/2−1/3 = 1/6. (5/6) ÷ (1/6) = 5. முக்கியக் கற்றல் கருத்து: ஒன்றை மற்றொன்றால் வகுக்கும் முன், ஒவ்வோர் அடைப்புக்குறியையும் ஒரே பின்னமாக முழுமையாகச் சுருக்கவும்."),
        # Q14
        ("சுருக்குக: 3.6 ÷ 1.2 + 2.5 × 2",
         ["6", "7", "8", "9"], 2,
         "3.6÷1.2=3. 2.5×2=5. 3+5 = 8. முக்கியக் கற்றல் கருத்து: தசம எண்களாக இருந்தாலும், கூட்டலுக்கு முன் வகுத்தலையும் பெருக்கலையும் செய்யவும்."),
        # Q15
        ("√50-ஐ அதன் எளிய மூல வடிவுக்குச் சுருக்குக.",
         ["2√5", "4√5", "5√2", "10√5"], 2,
         "50 = 25×2. √50 = √25×√2 = 5√2. முக்கியக் கற்றல் கருத்து: ஒரு முறுடைச் சுருக்க, மூலக்குறிக்குள் உள்ள மிகப்பெரிய முழு வர்க்கக் காரணியை வெளியே எடுக்கவும்."),
        # Q16
        ("சுருக்குக: a²b³ × a³b²",
         ["a⁵b⁵", "a⁶b⁶", "a⁵b⁶", "a⁶b⁵"], 0,
         "ஒரே அடிமானங்களின் அடுக்குகளைக் கூட்டவும்: a^(2+3) b^(3+2) = a⁵b⁵. முக்கியக் கற்றல் கருத்து: பல மாறி அடிமானங்கள் கொண்ட உறுப்புகளைப் பெருக்கும்போது, ஒவ்வோர் அடிமானத்துக்கும் தனித்தனியாக அடுக்குகளைக் கூட்டவும்."),
        # Q17
        ("சுருக்குக: 2 1/3 + 1 1/2",
         ["3 1/6", "3 5/6", "4 1/6", "4 5/6"], 1,
         "2 1/3 = 7/3, 1 1/2 = 3/2. மீ.பொ.ம=6: 14/6 + 9/6 = 23/6 = 3 5/6. முக்கியக் கற்றல் கருத்து: கூட்டும் முன் கலப்பு எண்களைத் தகா பின்னங்களாக மாற்றி, இறுதியில் மீண்டும் கலப்பு எண்ணாக மாற்றவும்."),
        # Q18
        ("0.333… என்ற சுழல் தசமத்தைப் பின்னமாக எழுதுக.",
         ["1/2", "1/3", "1/4", "3/10"], 1,
         "0.333… = 1/3 (ஒரு நிலையான சுழல் தசம மாற்றம்). முக்கியக் கற்றல் கருத்து: 0.333… = 1/3, 0.666… = 2/3 போன்ற பொதுவான சுழல் தசமங்களை நேரடியாக மனப்பாடம் செய்வது பயனுள்ளது."),
        # Q19
        ("சுருக்குக: 1 ÷ (1/2 + 1/3 + 1/6)",
         ["1/2", "1", "3/2", "2"], 1,
         "1/2+1/3+1/6 = 3/6+2/6+1/6 = 6/6 = 1. பின்னர் 1÷1 = 1. முக்கியக் கற்றல் கருத்து: வெளிச் செயலைச் செய்யும் முன், அடைப்புக்குறியை முதலில் ஒரே மதிப்பாகத் தீர்க்கவும்."),
        # Q20
        ("சிக்கலான பின்னத்தைச் சுருக்குக: (2 + 1/3) ÷ (1 − 1/4)",
         ["7/3", "3/4", "28/9", "9/4"], 2,
         "2+1/3 = 7/3. 1−1/4 = 3/4. (7/3) ÷ (3/4) = 7/3 × 4/3 = 28/9. முக்கியக் கற்றல் கருத்து: சிக்கலான பின்னத்தில், வகுக்கும் முன் தொகுதியையும் பகுதியையும் தனித்தனியாக முழுமையாகச் சுருக்கவும்."),
        # Q21
        ("சுருக்குக: 64^(1/2) − 27^(1/3)",
         ["3", "4", "5", "6"], 2,
         "64^(1/2) = 8 (வர்க்கமூலம்). 27^(1/3) = 3 (கனமூலம்). 8−3 = 5. முக்கியக் கற்றல் கருத்து: 1/2 என்ற பின்ன அடுக்கு வர்க்கமூலத்தையும், 1/3 கனமூலத்தையும் குறிக்கிறது."),
        # Q22
        ("சுருக்குக: 2.25 × 4 − 1.5²",
         ["5.75", "6.25", "6.75", "7.25"], 2,
         "2.25×4 = 9. 1.5² = 2.25. 9−2.25 = 6.75. முக்கியக் கற்றல் கருத்து: தசமங்களாக இருந்தாலும் BODMAS-இன்படி, கழித்தலுக்கு முன் அடுக்குகளை மதிப்பிடவும்."),
        # Q23
        ("சுருக்குக: (3/5-இன் 25) + (2/7-இன் 49)",
         ["27", "28", "29", "30"], 2,
         "25-இன் 3/5 = 15. 49-இன் 2/7 = 14. 15+14 = 29. முக்கியக் கற்றல் கருத்து: பின்னக் கணக்குகளில் “-இன்” (of) என்பது பெருக்கலைக் குறிக்கிறது – இணைக்கும் முன் ஒவ்வொரு “-இன்” உறுப்பையும் தனித்தனியாகக் கணக்கிடவும்."),
        # Q24
        ("√99.8-இன் தோராய மதிப்பைக் காண்க (அருகிலுள்ள முழு எண்).",
         ["9", "10", "11", "12"], 1,
         "99.8 என்பது 100-க்கு மிக அருகில் உள்ளது; √100 = 10. முக்கியக் கற்றல் கருத்து: தோராயமாக்கலுக்கு, முதலில் எண்ணை அருகிலுள்ள முழு வர்க்கம்/கனத்துக்கு முழுமையாக்கி, பின்னர் கணக்கிடவும்."),
        # Q25
        ("சுருக்குக: [(3+2)² − (3−2)²] ÷ (3×2)",
         ["2", "3", "4", "5"], 2,
         "(5² − 1²) ÷ 6 = (25−1) ÷ 6 = 24÷6 = 4. முக்கியக் கற்றல் கருத்து: இக்கோவை (a+b)²−(a−b)² = 4ab என்ற முற்றொருமைக்கு ஓர் எடுத்துக்காட்டு; ab-ஆல் வகுத்தால் எப்போதும் சரியாக 4 கிடைக்கும் – இத்தகைய முற்றொருமைகளை அடையாளம் காண்பது கணக்கீட்டு நேரத்தை மிச்சப்படுத்துகிறது.")
    ]

    # 30 Independent Practice (English)
    indep_en = [
        # Q1
        ("Simplify: 20 − 12 ÷ 4 × 2",
         ["4", "14", "16", "26"], 1,
         "Division and multiplication, left to right: 12÷4=3, 3×2=6. Then 20 − 6 = 14. Key Learning Point: Subtraction written first is still done last – complete division and multiplication (left to right) before subtracting.", "EASY"),
        # Q2
        ("Simplify: (18 − 6) ÷ 3",
         ["3", "4", "5", "6"], 1,
         "18−6=12. 12÷3 = 4. Key Learning Point: Resolve the bracket before dividing.", "EASY"),
        # Q3
        ("Simplify: 5/6 − 1/3",
         ["1/2", "2/3", "4/3", "1/3"], 0,
         "LCM = 6: 5/6 − 2/6 = 3/6 = 1/2. Key Learning Point: Convert to a common denominator before subtracting, then reduce the answer to lowest terms.", "EASY"),
        # Q4
        ("Simplify: (3²)³",
         ["243", "729", "2187", "81"], 1,
         "Power of a power: multiply the exponents. (3²)³ = 3^(2×3) = 3⁶ = 729. Key Learning Point: For a power raised to another power, multiply the exponents: (aᵐ)ⁿ = aᵐⁿ.", "EASY"),
        # Q5
        ("Simplify: 1.2 − 0.35 + 0.05",
         ["0.8", "0.9", "0.95", "0.75"], 1,
         "Left to right: 1.2 − 0.35 = 0.85. Then 0.85 + 0.05 = 0.9. Key Learning Point: Addition and subtraction have equal precedence – work from left to right, keeping decimal points aligned.", "EASY"),
        # Q6
        ("Simplify: 36 ÷ 6 × 2",
         ["3", "6", "12", "18"], 2,
         "Left to right: 36÷6=6. 6×2 = 12. Key Learning Point: With no brackets, division and multiplication are performed left to right.", "EASY"),
        # Q7
        ("Simplify: 24 ÷ 4 × 3 + 6 − 8",
         ["14", "16", "18", "20"], 1,
         "24÷4=6, 6×3=18. Then 18+6=24, 24−8 = 16. Key Learning Point: Complete all division/multiplication (left to right) before addition/subtraction.", "EASY"),
        # Q8
        ("Simplify: [20 − (6 ÷ 2)] × 2",
         ["30", "32", "34", "36"], 2,
         "6÷2=3. 20−3=17. 17×2 = 34. Key Learning Point: Resolve the innermost bracket first, then the outer one.", "EASY"),
        # Q9
        ("Simplify: 3/5 + 2/3 − 1/15",
         ["1", "6/5", "7/5", "4/3"], 1,
         "LCM=15: 9/15+10/15−1/15 = 18/15 = 6/5. Key Learning Point: Convert to a common denominator before combining three or more fractions.", "EASY"),
        # Q10
        ("Simplify: 0.8 × 0.5 + 0.25",
         ["0.55", "0.6", "0.65", "0.7"], 2,
         "0.8×0.5=0.4. 0.4+0.25 = 0.65. Key Learning Point: Complete decimal multiplication before addition.", "EASY"),
        # Q11
        ("Simplify: 53² − 47²",
         ["500", "600", "650", "700"], 1,
         "Use a² − b² = (a + b)(a − b): (53 + 47)(53 − 47) = 100 × 6 = 600. Key Learning Point: Recognising the identity a² − b² = (a + b)(a − b) avoids squaring large numbers.", "EASY"),
        # Q12
        ("Simplify: √0.49 + √0.0016",
         ["0.74", "0.704", "0.11", "0.47"], 0,
         "√0.49 = 0.7 and √0.0016 = 0.04. 0.7 + 0.04 = 0.74. Key Learning Point: For terminating decimals that are exact perfect squares, grouping the decimal places in pairs helps fix the position of the decimal point in the root (e.g., 0.0016 → 0.04).", "EASY"),
        # Q13
        ("Simplify: 3⁴ × 3² ÷ 3⁵",
         ["1", "3", "9", "27"], 1,
         "3^(4+2−5) = 3^1 = 3. Key Learning Point: Combine multiple exponent operations on the same base into one exponent before evaluating.", "EASY"),
        # Q14
        ("Simplify: (1/3 + 1/4) ÷ (1/3 − 1/4)",
         ["5", "6", "7", "8"], 2,
         "1/3+1/4=7/12. 1/3−1/4=1/12. (7/12)÷(1/12) = 7. Key Learning Point: Simplify each bracket fully to a single fraction before dividing.", "EASY"),
        # Q15
        ("Simplify: 4.5 ÷ 1.5 + 3.2 × 2",
         ["8.4", "9.4", "10.4", "11.4"], 1,
         "4.5÷1.5=3. 3.2×2=6.4. 3+6.4 = 9.4. Key Learning Point: Perform division and multiplication before addition, even with decimals.", "EASY"),
        # Q16
        ("Simplify √72 into its simplest radical form.",
         ["4√3", "6√2", "8√3", "3√8"], 1,
         "72 = 36×2. √72 = √36×√2 = 6√2. Key Learning Point: Factor out the largest perfect square under the root to simplify a surd.", "EASY"),
        # Q17
        ("Simplify: x³y² × x²y⁴",
         ["x⁵y⁶", "x⁶y⁶", "x⁵y⁸", "x⁶y⁸"], 0,
         "x^(3+2) y^(2+4) = x⁵y⁶. Key Learning Point: Add exponents separately for each variable base.", "EASY"),
        # Q18
        ("Simplify: 3 1/4 + 2 1/3",
         ["5 5/12", "5 7/12", "6 1/12", "6 7/12"], 1,
         "3 1/4 = 13/4, 2 1/3 = 7/3. LCM=12: 39/12+28/12 = 67/12 = 5 7/12. Key Learning Point: Convert mixed numbers to improper fractions before combining.", "EASY"),
        # Q19
        ("Express the recurring decimal 0.666… as a fraction.",
         ["1/2", "2/3", "3/4", "2/5"], 1,
         "0.666… = 2/3. Key Learning Point: 0.666… is the recurring-decimal form of 2/3, the complement pattern to 0.333… = 1/3.", "EASY"),
        # Q20
        ("Simplify: 1 ÷ (1/3 + 1/4 + 1/12)",
         ["1", "3/2", "2", "5/2"], 1,
         "1/3+1/4+1/12 = 4/12+3/12+1/12 = 8/12 = 2/3. 1÷(2/3) = 3/2. Key Learning Point: Simplify the bracket to a single fraction, then invert and multiply for the division.", "EASY"),
        # Q21
        ("Simplify the complex fraction: (3 + 1/2) ÷ (2 − 1/4)",
         ["1", "2", "7/4", "7/2"], 1,
         "3+1/2 = 7/2. 2−1/4 = 7/4. (7/2) ÷ (7/4) = 7/2 × 4/7 = 2. Key Learning Point: Simplify the numerator and denominator of a complex fraction fully before dividing.", "EASY"),
        # Q22
        ("Simplify: 125^(1/3) − 16^(1/2)",
         ["1", "2", "3", "4"], 0,
         "125^(1/3) = 5. 16^(1/2) = 4. 5−4 = 1. Key Learning Point: 1/3 as an exponent means cube root; 1/2 means square root.", "EASY"),
        # Q23
        ("Simplify: 3.5 × 2 − 1.2²",
         ["4.56", "5.56", "6.56", "7.56"], 1,
         "3.5×2=7. 1.2²=1.44. 7−1.44 = 5.56. Key Learning Point: Compute powers before subtraction, even with decimal bases.", "EASY"),
        # Q24
        ("Simplify: (2/5 of 40) + (3/8 of 64)",
         ["38", "39", "40", "41"], 2,
         "2/5 of 40 = 16. 3/8 of 64 = 24. 16+24 = 40. Key Learning Point: Compute each “of” term as a separate multiplication before combining.", "EASY"),
        # Q25
        ("Find the approximate value of √80.5 (nearest whole number).",
         ["8", "9", "10", "11"], 1,
         "80.5 is close to 81, and √81 = 9. Key Learning Point: Round to the nearest perfect square before estimating a square root.", "EASY"),
        # Q26
        ("Simplify: 7.5² − 2 × 7.5 × 2.5 + 2.5²",
         ["25", "50", "100", "10"], 0,
         "This is a² − 2ab + b² = (a − b)² with a = 7.5, b = 2.5. (7.5 − 2.5)² = 5² = 25. Key Learning Point: Spotting the identity (a − b)² = a² − 2ab + b² turns a long decimal calculation into one step.", "MEDIUM"),
        # Q27
        ("Simplify: 2/7 + 3/14 − 1/2",
         ["−1/14", "0", "1/14", "1/7"], 1,
         "LCM=14: 4/14+3/14−7/14 = 0/14 = 0. Key Learning Point: A simplification can validly result in zero – don’t assume an error if the terms cancel out.", "EASY"),
        # Q28
        ("Simplify: 0.45 × 0.2 + 0.19",
         ["0.25", "0.28", "0.3", "0.33"], 1,
         "0.45×0.2=0.09. 0.09+0.19 = 0.28. Key Learning Point: Complete decimal multiplication before addition, per BODMAS.", "EASY"),
        # Q29
        ("Simplify: 8² − 4³ ÷ 2",
         ["16", "24", "32", "40"], 2,
         "4³=64, 64÷2=32. 8²=64. 64−32 = 32. Key Learning Point: Evaluate all powers and division before subtraction.", "EASY"),
        # Q30
        ("Simplify: 5³ ÷ 5² + 5",
         ["5", "8", "10", "15"], 2,
         "5³÷5² = 5^(3−2) = 5. Then 5+5 = 10. Key Learning Point: Simplify exponent division first using the subtraction-of-exponents rule, then complete the addition.", "EASY")
    ]

    # 30 Independent Practice (Tamil)
    indep_ta = [
        # Q1
        ("சுருக்குக: 20 − 12 ÷ 4 × 2",
         ["4", "14", "16", "26"], 1,
         "வகுத்தலும் பெருக்கலும், இடமிருந்து வலமாக: 12÷4=3, 3×2=6. பின்னர் 20 − 6 = 14. முக்கியக் கற்றல் கருத்து: முதலில் எழுதப்பட்ட கழித்தல் இறுதியிலேயே செய்யப்படுகிறது – கழிக்கும் முன் வகுத்தலையும் பெருக்கலையும் (இடமிருந்து வலமாக) முடிக்கவும்."),
        # Q2
        ("சுருக்குக: (18 − 6) ÷ 3",
         ["3", "4", "5", "6"], 1,
         "18−6=12. 12÷3 = 4. முக்கியக் கற்றல் கருத்து: வகுக்கும் முன் அடைப்புக்குறியைத் தீர்க்கவும்."),
        # Q3
        ("சுருக்குக: 5/6 − 1/3",
         ["1/2", "2/3", "4/3", "1/3"], 0,
         "மீ.பொ.ம = 6: 5/6 − 2/6 = 3/6 = 1/2. முக்கியக் கற்றல் கருத்து: கழிக்கும் முன் பொதுப் பகுதிக்கு மாற்றி, விடையை அதன் எளிய வடிவுக்குச் சுருக்கவும்."),
        # Q4
        ("சுருக்குக: (3²)³",
         ["243", "729", "2187", "81"], 1,
         "அடுக்கின் அடுக்கு: அடுக்குகளைப் பெருக்கவும். (3²)³ = 3^(2×3) = 3⁶ = 729. முக்கியக் கற்றல் கருத்து: ஓர் அடுக்கை மற்றோர் அடுக்குக்கு உயர்த்தும்போது, அடுக்குகளைப் பெருக்கவும்: (aᵐ)ⁿ = aᵐⁿ."),
        # Q5
        ("சுருக்குக: 1.2 − 0.35 + 0.05",
         ["0.8", "0.9", "0.95", "0.75"], 1,
         "இடமிருந்து வலமாக: 1.2 − 0.35 = 0.85. பின்னர் 0.85 + 0.05 = 0.9. முக்கியக் கற்றல் கருத்து: கூட்டலும் கழித்தலும் சம முன்னுரிமை உடையவை – தசமப் புள்ளிகளை நேராக வைத்து இடமிருந்து வலமாகச் செயல்படவும்."),
        # Q6
        ("சுருக்குக: 36 ÷ 6 × 2",
         ["3", "6", "12", "18"], 2,
         "இடமிருந்து வலமாக: 36÷6=6. 6×2 = 12. முக்கியக் கற்றல் கருத்து: அடைப்புக்குறிகள் இல்லாதபோது, வகுத்தலும் பெருக்கலும் இடமிருந்து வலமாகச் செய்யப்படுகின்றன."),
        # Q7
        ("சுருக்குக: 24 ÷ 4 × 3 + 6 − 8",
         ["14", "16", "18", "20"], 1,
         "24÷4=6, 6×3=18. பின்னர் 18+6=24, 24−8 = 16. முக்கியக் கற்றல் கருத்து: கூட்டல்/கழித்தலுக்கு முன் அனைத்து வகுத்தல்/பெருக்கலையும் (இடமிருந்து வலமாக) முடிக்கவும்."),
        # Q8
        ("சுருக்குக: [20 − (6 ÷ 2)] × 2",
         ["30", "32", "34", "36"], 2,
         "6÷2=3. 20−3=17. 17×2 = 34. முக்கியக் கற்றல் கருத்து: முதலில் உள்ளார்ந்த அடைப்புக்குறியையும், பின்னர் வெளி அடைப்புக்குறியையும் தீர்க்கவும்."),
        # Q9
        ("சுருக்குக: 3/5 + 2/3 − 1/15",
         ["1", "6/5", "7/5", "4/3"], 1,
         "மீ.பொ.ம=15: 9/15+10/15−1/15 = 18/15 = 6/5. முக்கியக் கற்றல் கருத்து: மூன்று அல்லது அதற்கு மேற்பட்ட பின்னங்களை இணைக்கும் முன் பொதுப் பகுதிக்கு மாற்றவும்."),
        # Q10
        ("சுருக்குக: 0.8 × 0.5 + 0.25",
         ["0.55", "0.6", "0.65", "0.7"], 2,
         "0.8×0.5=0.4. 0.4+0.25 = 0.65. முக்கியக் கற்றல் கருத்து: கூட்டலுக்கு முன் தசமப் பெருக்கலை முடிக்கவும்."),
        # Q11
        ("சுருக்குக: 53² − 47²",
         ["500", "600", "650", "700"], 1,
         "a² − b² = (a + b)(a − b) என்பதைப் பயன்படுத்தவும்: (53 + 47)(53 − 47) = 100 × 6 = 600. முக்கியக் கற்றல் கருத்து: a² − b² = (a + b)(a − b) என்ற முற்றொருமையை அடையாளம் காண்பது பெரிய எண்களை வர்க்கப்படுத்துவதைத் தவிர்க்கிறது."),
        # Q12
        ("சுருக்குக: √0.49 + √0.0016",
         ["0.74", "0.704", "0.11", "0.47"], 0,
         "√0.49 = 0.7, √0.0016 = 0.04. 0.7 + 0.04 = 0.74. முக்கியக் கற்றல் கருத்து: சரியான முழு வர்க்கங்களாக உள்ள முடிவுறு தசமங்களுக்கு, தசம இடங்களை இரண்டிரண்டாகக் குழுவாக்குவது மூலத்தில் தசமப் புள்ளியின் இடத்தை நிர்ணயிக்க உதவுகிறது (எ.கா., 0.0016 → 0.04)."),
        # Q13
        ("சுருக்குக: 3⁴ × 3² ÷ 3⁵",
         ["1", "3", "9", "27"], 1,
         "3^(4+2−5) = 3^1 = 3. முக்கியக் கற்றல் கருத்து: மதிப்பிடும் முன், ஒரே அடிமானத்தின் மீதான பல அடுக்குச் செயல்களை ஒரே அடுக்காக இணைக்கவும்."),
        # Q14
        ("சுருக்குக: (1/3 + 1/4) ÷ (1/3 − 1/4)",
         ["5", "6", "7", "8"], 2,
         "1/3+1/4=7/12. 1/3−1/4=1/12. (7/12)÷(1/12) = 7. முக்கியக் கற்றல் கருத்து: வகுக்கும் முன், ஒவ்வோர் அடைப்புக்குறியையும் ஒரே பின்னமாக முழுமையாகச் சுருக்கவும்."),
        # Q15
        ("சுருக்குக: 4.5 ÷ 1.5 + 3.2 × 2",
         ["8.4", "9.4", "10.4", "11.4"], 1,
         "4.5÷1.5=3. 3.2×2=6.4. 3+6.4 = 9.4. முக்கியக் கற்றல் கருத்து: தசமங்களாக இருந்தாலும், கூட்டலுக்கு முன் வகுத்தலையும் பெருக்கலையும் செய்யவும்."),
        # Q16
        ("√72-ஐ அதன் எளிய மூல வடிவுக்குச் சுருக்குக.",
         ["4√3", "6√2", "8√3", "3√8"], 1,
         "72 = 36×2. √72 = √36×√2 = 6√2. முக்கியக் கற்றல் கருத்து: ஒரு முறுடைச் சுருக்க, மூலக்குறிக்குள் உள்ள மிகப்பெரிய முழு வர்க்கக் காரணியை வெளியே எடுக்கவும்."),
        # Q17
        ("சுருக்குக: x³y² × x²y⁴",
         ["x⁵y⁶", "x⁶y⁶", "x⁵y⁸", "x⁶y⁸"], 0,
         "x^(3+2) y^(2+4) = x⁵y⁶. முக்கியக் கற்றல் கருத்து: ஒவ்வொரு மாறி அடிமானத்துக்கும் தனித்தனியாக அடுக்குகளைக் கூட்டவும்."),
        # Q18
        ("சுருக்குக: 3 1/4 + 2 1/3",
         ["5 5/12", "5 7/12", "6 1/12", "6 7/12"], 1,
         "3 1/4 = 13/4, 2 1/3 = 7/3. மீ.பொ.ம=12: 39/12+28/12 = 67/12 = 5 7/12. முக்கியக் கற்றல் கருத்து: இணைக்கும் முன் கலப்பு எண்களைத் தகா பின்னங்களாக மாற்றவும்."),
        # Q19
        ("0.666… என்ற சுழல் தசமத்தைப் பின்னமாக எழுதுக.",
         ["1/2", "2/3", "3/4", "2/5"], 1,
         "0.666… = 2/3. முக்கியக் கற்றல் கருத்து: 0.666… என்பது 2/3-இன் சுழல் தசம வடிவம்; இது 0.333… = 1/3 என்பதன் நிரப்பு அமைப்பு."),
        # Q20
        ("சுருக்குக: 1 ÷ (1/3 + 1/4 + 1/12)",
         ["1", "3/2", "2", "5/2"], 1,
         "1/3+1/4+1/12 = 4/12+3/12+1/12 = 8/12 = 2/3. 1÷(2/3) = 3/2. முக்கியக் கற்றல் கருத்து: அடைப்புக்குறியை ஒரே பின்னமாகச் சுருக்கி, பின்னர் வகுத்தலுக்குத் தலைகீழாக்கிப் பெருக்கவும்."),
        # Q21
        ("சிக்கலான பின்னத்தைச் சுருக்குக: (3 + 1/2) ÷ (2 − 1/4)",
         ["1", "2", "7/4", "7/2"], 1,
         "3+1/2 = 7/2. 2−1/4 = 7/4. (7/2) ÷ (7/4) = 7/2 × 4/7 = 2. முக்கியக் கற்றல் கருத்து: சிக்கலான பின்னத்தின் தொகுதியையும் பகுதியையும் வகுக்கும் முன் முழுமையாகச் சுருக்கவும்."),
        # Q22
        ("சுருக்குக: 125^(1/3) − 16^(1/2)",
         ["1", "2", "3", "4"], 0,
         "125^(1/3) = 5. 16^(1/2) = 4. 5−4 = 1. முக்கியக் கற்றல் கருத்து: அடுக்காக வரும் 1/3 கனமூலத்தையும், 1/2 வர்க்கமூலத்தையும் குறிக்கிறது."),
        # Q23
        ("சுருக்குக: 3.5 × 2 − 1.2²",
         ["4.56", "5.56", "6.56", "7.56"], 1,
         "3.5×2=7. 1.2²=1.44. 7−1.44 = 5.56. முக்கியக் கற்றல் கருத்து: தசம அடிமானங்களாக இருந்தாலும், கழித்தலுக்கு முன் அடுக்குகளைக் கணக்கிடவும்."),
        # Q24
        ("சுருக்குக: (2/5-இன் 40) + (3/8-இன் 64)",
         ["38", "39", "40", "41"], 2,
         "40-இன் 2/5 = 16. 64-இன் 3/8 = 24. 16+24 = 40. முக்கியக் கற்றல் கருத்து: இணைக்கும் முன், ஒவ்வொரு “-இன்” உறுப்பையும் தனிப்பெருக்கலாகக் கணக்கிடவும்."),
        # Q25
        ("√80.5-இன் தோராய மதிப்பைக் காண்க (அருகிலுள்ள முழு எண்).",
         ["8", "9", "10", "11"], 1,
         "80.5 என்பது 81-க்கு அருகில் உள்ளது; √81 = 9. முக்கியக் கற்றல் கருத்து: வர்க்கமூலத்தை மதிப்பிடும் முன் அருகிலுள்ள முழு வர்க்கத்துக்கு முழுமையாக்கவும்."),
        # Q26
        ("சுருக்குக: 7.5² − 2 × 7.5 × 2.5 + 2.5²",
         ["25", "50", "100", "10"], 0,
         "இது a = 7.5, b = 2.5 உடன் a² − 2ab + b² = (a − b)² ஆகும். (7.5 − 2.5)² = 5² = 25. முக்கியக் கற்றல் கருத்து: (a − b)² = a² − 2ab + b² என்ற முற்றொருமையைக் கண்டறிவது நீண்ட தசமக் கணக்கீட்டை ஒரே படியாக்குகிறது."),
        # Q27
        ("சுருக்குக: 2/7 + 3/14 − 1/2",
         ["−1/14", "0", "1/14", "1/7"], 1,
         "மீ.பொ.ம=14: 4/14+3/14−7/14 = 0/14 = 0. முக்கியக் கற்றல் கருத்து: சுருக்குதலின் விடை சரியாகவே பூஜ்ஜியமாக இருக்கலாம் – உறுப்புகள் நீங்கினால் பிழை எனக் கருத வேண்டாம்."),
        # Q28
        ("சுருக்குக: 0.45 × 0.2 + 0.19",
         ["0.25", "0.28", "0.3", "0.33"], 1,
         "0.45×0.2=0.09. 0.09+0.19 = 0.28. முக்கியக் கற்றல் கருத்து: BODMAS-இன்படி, கூட்டலுக்கு முன் தசமப் பெருக்கலை முடிக்கவும்."),
        # Q29
        ("சுருக்குக: 8² − 4³ ÷ 2",
         ["16", "24", "32", "40"], 2,
         "4³=64, 64÷2=32. 8²=64. 64−32 = 32. முக்கியக் கற்றல் கருத்து: கழித்தலுக்கு முன் அனைத்து அடுக்குகளையும் வகுத்தலையும் மதிப்பிடவும்."),
        # Q30
        ("சுருக்குக: 5³ ÷ 5² + 5",
         ["5", "8", "10", "15"], 2,
         "5³÷5² = 5^(3−2) = 5. பின்னர் 5+5 = 10. முக்கியக் கற்றல் கருத்து: அடுக்குகளைக் கழிக்கும் விதியைப் பயன்படுத்தி முதலில் அடுக்கு வகுத்தலைச் சுருக்கி, பின்னர் கூட்டலை முடிக்கவும்.")
    ]

    # 30 Assessment Questions (English)
    assess_en = [
        # Q1
        ("Simplify: 48 ÷ 4 − 2 × 3 + 5",
         ["9", "11", "13", "17"], 1,
         "Division and multiplication first: 48 ÷ 4 = 12, 2 × 3 = 6. Then left to right: 12 − 6 + 5 = 11. Key Learning Point: Complete all division and multiplication before any addition or subtraction.", "EASY"),
        # Q2
        ("Simplify: 7 − [3 + (8 − 2 × 3)] × 2",
         ["3", "−3", "−13", "8"], 1,
         "Innermost bracket: 8 − 2×3 = 8 − 6 = 2. Square bracket: 3 + 2 = 5. Then 5 × 2 = 10. 7 − 10 = −3. Key Learning Point: Resolve brackets from the innermost outward, and do not fear a negative final answer.", "MEDIUM"),
        # Q3
        ("Simplify: 5/6 − 3/8 + 1/4",
         ["13/24", "7/12", "19/24", "17/24"], 3,
         "LCM of 6, 8, 4 = 24: 20/24 − 9/24 + 6/24 = 17/24. Key Learning Point: Use the LCM of all denominators, then combine the numerators from left to right.", "EASY"),
        # Q4
        ("Simplify: (3/4 × 8/9) ÷ 2/3",
         ["1/2", "1", "4/3", "3/2"], 1,
         "3/4 × 8/9 = 24/36 = 2/3. 2/3 ÷ 2/3 = 2/3 × 3/2 = 1. Key Learning Point: Cancel common factors before multiplying fractions; dividing by a fraction means multiplying by its reciprocal.", "EASY"),
        # Q5
        ("Simplify: √(0.3² + 0.4²)",
         ["0.35", "0.7", "0.25", "0.5"], 3,
         "0.3² = 0.09, 0.4² = 0.16. Sum = 0.25. √0.25 = 0.5. Key Learning Point: Evaluate the powers inside the root first; the root applies to the whole sum, not to each term separately.", "EASY"),
        # Q6
        ("Simplify: 1.25 × 0.8 ÷ 0.5",
         ["2", "1", "0.5", "2.5"], 0,
         "Left to right: 1.25 × 0.8 = 1. 1 ÷ 0.5 = 2. Key Learning Point: Multiplication and division have equal precedence – work from left to right.", "EASY"),
        # Q7
        ("Simplify: (2³)² ÷ 2⁴",
         ["2", "4", "8", "16"], 1,
         "(2³)² = 2⁶ (multiply exponents). 2⁶ ÷ 2⁴ = 2^(6−4) = 2² = 4. Key Learning Point: Apply the power-of-a-power rule first, then the division rule for like bases.", "EASY"),
        # Q8
        ("Simplify: 3⁻² × 27",
         ["3", "1/3", "9", "1/9"], 0,
         "3⁻² = 1/3² = 1/9. 1/9 × 27 = 3. Key Learning Point: A negative exponent means the reciprocal: a⁻ⁿ = 1/aⁿ.", "EASY"),
        # Q9
        ("Simplify: 5⁰ + 4⁰ × 2",
         ["1", "3", "2", "9"], 1,
         "Any non-zero number to the power 0 is 1: 5⁰ = 1, 4⁰ = 1. 1 + 1 × 2 = 1 + 2 = 3. Key Learning Point: a⁰ = 1 for any non-zero a; then continue with BODMAS as usual.", "EASY"),
        # Q10
        ("Simplify: √18 + √32",
         ["7√2", "5√2", "√50", "12√2"], 0,
         "√18 = √(9×2) = 3√2; √32 = √(16×2) = 4√2. 3√2 + 4√2 = 7√2. Key Learning Point: Surds can be added only after they are simplified to the same radical (like terms).", "EASY"),
        # Q11
        ("Simplify: √12 × √3",
         ["36", "9", "12", "6"], 3,
         "√12 × √3 = √(12 × 3) = √36 = 6. Key Learning Point: Multiply surds by multiplying the numbers under the roots: √a × √b = √(ab).", "EASY"),
        # Q12
        ("Simplify: (√5 + √3)(√5 − √3)",
         ["√2", "8", "2", "4"], 2,
         "Use (a + b)(a − b) = a² − b². (√5)² − (√3)² = 5 − 3 = 2. Key Learning Point: The difference-of-squares identity removes the surds completely.", "EASY"),
        # Q13
        ("Rationalise and simplify: 1 / (√2 + 1)",
         ["√2 + 1", "1 − √2", "√2 − 1", "2√2"], 2,
         "Multiply numerator and denominator by (√2 − 1). (√2 − 1) / [(√2)² − 1²] = (√2 − 1) / 1 = √2 − 1. Key Learning Point: To rationalise a denominator of the form √a + b, multiply by its conjugate √a − b.", "MEDIUM"),
        # Q14
        ("Express 0.1666… (only 6 recurring) as a fraction.",
         ["1/5", "16/99", "1/6", "3/20"], 2,
         "Let x = 0.1666… Then 100x = 16.666… and 10x = 1.666… 90x = 15, so x = 15/90 = 1/6. Key Learning Point: For a mixed recurring decimal, subtract to remove the recurring part: (all digits − non-recurring digits) / (9s and 0s).", "MEDIUM"),
        # Q15
        ("Simplify: 0.333… + 0.666…",
         ["0.9", "0.99", "10/9", "1"], 3,
         "0.333… = 1/3 and 0.666… = 2/3. 1/3 + 2/3 = 1. Key Learning Point: Convert recurring decimals to fractions before adding – the exact sum may differ from a truncated decimal sum.", "EASY"),
        # Q16
        ("Express the recurring decimal 0.454545… as a fraction in lowest terms.",
         ["5/11", "9/20", "45/100", "4/9"], 0,
         "Two digits recur, so 0.4545… = 45/99. 45/99 = 5/11 (dividing by 9). Key Learning Point: For a pure recurring decimal, write the recurring block over as many 9s as it has digits, then reduce.", "MEDIUM"),
        # Q17
        ("Simplify: 1 + 1/(1 + 1/(1 + 1/2))",
         ["5/3", "3/2", "13/8", "8/5"], 3,
         "Innermost: 1 + 1/2 = 3/2. Next: 1 + 1/(3/2) = 1 + 2/3 = 5/3. Outer: 1 + 1/(5/3) = 1 + 3/5 = 8/5. Key Learning Point: Simplify a continued fraction from the bottom (innermost) level upward.", "MEDIUM"),
        # Q18
        ("Simplify: (1 − 1/2)(1 − 1/3)(1 − 1/4)(1 − 1/5)",
         ["1/120", "1/4", "1/5", "4/5"], 2,
         "Each bracket: 1/2 × 2/3 × 3/4 × 4/5. Numerators and denominators cancel in a chain, leaving 1/5. Key Learning Point: Look for cancelling (telescoping) products before multiplying everything out.", "MEDIUM"),
        # Q19
        ("Simplify: 1/(1×2) + 1/(2×3) + 1/(3×4) + 1/(4×5)",
         ["4/5", "5/6", "1/2", "1"], 0,
         "Use 1/(n(n+1)) = 1/n − 1/(n+1). Sum = (1 − 1/2) + (1/2 − 1/3) + (1/3 − 1/4) + (1/4 − 1/5) = 1 − 1/5 = 4/5. Key Learning Point: Splitting each term into a difference makes the middle terms cancel (telescoping sum).", "MEDIUM"),
        # Q20
        ("Simplify: 0.5² ÷ 0.05",
         ["0.5", "5", "50", "0.05"], 1,
         "0.5² = 0.25. 0.25 ÷ 0.05 = 25 ÷ 5 = 5. Key Learning Point: Evaluate the power first; to divide decimals, multiply both numbers by the same power of 10.", "EASY"),
        # Q21
        ("Simplify: 999 × 999 + 999",
         ["998001", "999999", "999000", "1000000"], 2,
         "Take 999 as a common factor: 999 × (999 + 1) = 999 × 1000 = 999000. Key Learning Point: Factorising a common term (distributive law) is faster than multiplying large numbers.", "EASY"),
        # Q22
        ("Simplify: 1.1 + 1.01 + 1.001",
         ["3.3", "3.011", "3.101", "3.111"], 3,
         "Align the decimal points: 1.100 + 1.010 + 1.001 = 3.111. Key Learning Point: Write every decimal to the same number of places before adding.", "EASY"),
        # Q23
        ("Simplify: (1.5³ − 0.5³) ÷ (1.5² + 1.5 × 0.5 + 0.5²)",
         ["0.5", "1.5", "2", "1"], 3,
         "Use a³ − b³ = (a − b)(a² + ab + b²) with a = 1.5, b = 0.5. The denominator cancels, leaving a − b = 1.5 − 0.5 = 1. Key Learning Point: Recognise standard identities in the structure of the expression before computing.", "MEDIUM"),
        # Q24
        ("Simplify: 40% of 250 − 3/4 of 80",
         ["20", "40", "60", "80"], 1,
         "40% of 250 = 0.4 × 250 = 100. 3/4 of 80 = 60. 100 − 60 = 40. Key Learning Point: “Of” means multiplication for both percentages and fractions; evaluate each term before subtracting.", "EASY"),
        # Q25
        ("Simplify: √(64.8 ÷ 0.2)",
         ["16", "20", "18", "24"], 2,
         "64.8 ÷ 0.2 = 648 ÷ 2 = 324. √324 = 18. Key Learning Point: Complete the operation under the root sign before taking the square root.", "EASY"),
        # Q26
        ("Find the approximate value of 49.97 × 20.02 ÷ 9.99.",
         ["90", "100", "110", "1000"], 1,
         "Approximate each number to a convenient value: 50 × 20 ÷ 10 = 1000 ÷ 10 = 100. Key Learning Point: For estimation, round each number to a nearby convenient value once, then compute.", "EASY"),
        # Q27
        ("Simplify: ∛0.008 + √0.09",
         ["0.5", "0.05", "0.23", "0.35"], 0,
         "∛0.008 = 0.2 (since 0.2³ = 0.008). √0.09 = 0.3. 0.2 + 0.3 = 0.5. Key Learning Point: For terminating decimals that are exact perfect squares or perfect cubes, grouping decimal places appropriately (in pairs for square roots, in threes for cube roots) helps determine the position of the decimal point in the root.", "EASY"),
        # Q28
        ("If 2ˣ = 32, find the value of 3^(x − 2).",
         ["27", "9", "81", "243"], 0,
         "32 = 2⁵, so x = 5. 3^(5 − 2) = 3³ = 27. Key Learning Point: Write both sides with the same base to find the unknown exponent.", "EASY"),
        # Q29
        ("Simplify: 81^0.25 × 16^0.75",
         ["24", "18", "12", "36"], 0,
         "81^0.25 = 81^(1/4) = 3. 16^0.75 = 16^(3/4) = (2)³ = 8. 3 × 8 = 24. Key Learning Point: Convert decimal exponents to fractions: 0.25 = 1/4 (fourth root) and 0.75 = 3/4 (fourth root, then cube).", "MEDIUM"),
        # Q30
        ("Simplify: (0.2² + 0.1²) ÷ 0.05",
         ["0.1", "10", "1", "0.5"], 2,
         "0.2² = 0.04, 0.1² = 0.01. Sum = 0.05. 0.05 ÷ 0.05 = 1. Key Learning Point: Evaluate powers inside the bracket first, then divide.", "EASY")
    ]

    # 30 Assessment Questions (Tamil)
    assess_ta = [
        # Q1
        ("சுருக்குக: 48 ÷ 4 − 2 × 3 + 5",
         ["9", "11", "13", "17"], 1,
         "முதலில் வகுத்தலும் பெருக்கலும்: 48 ÷ 4 = 12, 2 × 3 = 6. பின்னர் இடமிருந்து வலமாக: 12 − 6 + 5 = 11. முக்கியக் கற்றல் கருத்து: எந்தக் கூட்டல் அல்லது கழித்தலுக்கும் முன் அனைத்து வகுத்தலையும் பெருக்கலையும் முடிக்கவும்."),
        # Q2
        ("சுருக்குக: 7 − [3 + (8 − 2 × 3)] × 2",
         ["3", "−3", "−13", "8"], 1,
         "உள்ளார்ந்த அடைப்புக்குறி: 8 − 2×3 = 8 − 6 = 2. சதுர அடைப்புக்குறி: 3 + 2 = 5. பின்னர் 5 × 2 = 10. 7 − 10 = −3. முக்கியக் கற்றல் கருத்து: அடைப்புக்குறிகளை உள்ளார்ந்ததிலிருந்து வெளிநோக்கித் தீர்க்கவும்; இறுதி விடை எதிர்மறையாக வந்தாலும் அஞ்ச வேண்டாம்."),
        # Q3
        ("சுருக்குக: 5/6 − 3/8 + 1/4",
         ["13/24", "7/12", "19/24", "17/24"], 3,
         "6, 8, 4-இன் மீ.பொ.ம = 24: 20/24 − 9/24 + 6/24 = 17/24. முக்கியக் கற்றல் கருத்து: அனைத்துப் பகுதிகளின் மீ.பொ.ம-வைப் பயன்படுத்தி, தொகுதிகளை இடமிருந்து வலமாக இணைக்கவும்."),
        # Q4
        ("சுருக்குக: (3/4 × 8/9) ÷ 2/3",
         ["1/2", "1", "4/3", "3/2"], 1,
         "3/4 × 8/9 = 24/36 = 2/3. 2/3 ÷ 2/3 = 2/3 × 3/2 = 1. முக்கியக் கற்றல் கருத்து: பின்னங்களைப் பெருக்கும் முன் பொதுக் காரணிகளை நீக்கவும்; ஒரு பின்னத்தால் வகுப்பது என்பது அதன் தலைகீழியால் பெருக்குவதாகும்."),
        # Q5
        ("சுருக்குக: √(0.3² + 0.4²)",
         ["0.35", "0.7", "0.25", "0.5"], 3,
         "0.3² = 0.09, 0.4² = 0.16. கூடுதல் = 0.25. √0.25 = 0.5. முக்கியக் கற்றல் கருத்து: மூலக்குறிக்குள் உள்ள அடுக்குகளை முதலில் மதிப்பிடவும்; மூலம் ஒவ்வோர் உறுப்புக்கும் தனித்தனியாக அல்லாமல், முழுக் கூடுதலுக்கும் பொருந்தும்."),
        # Q6
        ("சுருக்குக: 1.25 × 0.8 ÷ 0.5",
         ["2", "1", "0.5", "2.5"], 0,
         "இடமிருந்து வலமாக: 1.25 × 0.8 = 1. 1 ÷ 0.5 = 2. முக்கியக் கற்றல் கருத்து: பெருக்கலும் வகுத்தலும் சம முன்னுரிமை உடையவை – இடமிருந்து வலமாகச் செயல்படவும்."),
        # Q7
        ("சுருக்குக: (2³)² ÷ 2⁴",
         ["2", "4", "8", "16"], 1,
         "(2³)² = 2⁶ (அடுக்குகளைப் பெருக்கவும்). 2⁶ ÷ 2⁴ = 2^(6−4) = 2² = 4. முக்கியக் கற்றல் கருத்து: முதலில் அடுக்கின் அடுக்கு விதியையும், பின்னர் ஒரே அடிமானங்களின் வகுத்தல் விதியையும் பயன்படுத்தவும்."),
        # Q8
        ("சுருக்குக: 3⁻² × 27",
         ["3", "1/3", "9", "1/9"], 0,
         "3⁻² = 1/3² = 1/9. 1/9 × 27 = 3. முக்கியக் கற்றல் கருத்து: எதிர்மறை அடுக்கு தலைகீழியைக் குறிக்கிறது: a⁻ⁿ = 1/aⁿ."),
        # Q9
        ("சுருக்குக: 5⁰ + 4⁰ × 2",
         ["1", "3", "2", "9"], 1,
         "பூஜ்ஜியம் அல்லாத எந்த எண்ணின் 0 அடுக்கும் 1: 5⁰ = 1, 4⁰ = 1. 1 + 1 × 2 = 1 + 2 = 3. முக்கியக் கற்றல் கருத்து: பூஜ்ஜியம் அல்லாத எந்த a-க்கும் a⁰ = 1; பின்னர் வழக்கம்போல் BODMAS-ஐத் தொடரவும்."),
        # Q10
        ("சுருக்குக: √18 + √32",
         ["7√2", "5√2", "√50", "12√2"], 0,
         "√18 = √(9×2) = 3√2; √32 = √(16×2) = 4√2. 3√2 + 4√2 = 7√2. முக்கியக் கற்றல் கருத்து: முறுடுகளை ஒரே மூல வடிவுக்கு (ஒத்த உறுப்புகள்) சுருக்கிய பின்னரே கூட்ட முடியும்."),
        # Q11
        ("சுருக்குக: √12 × √3",
         ["36", "9", "12", "6"], 3,
         "√12 × √3 = √(12 × 3) = √36 = 6. முக்கியக் கற்றல் கருத்து: மூலக்குறிக்குள் உள்ள எண்களைப் பெருக்கி முறுடுகளைப் பெருக்கவும்: √a × √b = √(ab)."),
        # Q12
        ("சுருக்குக: (√5 + √3)(√5 − √3)",
         ["√2", "8", "2", "4"], 2,
         "(a + b)(a − b) = a² − b² என்பதைப் பயன்படுத்தவும். (√5)² − (√3)² = 5 − 3 = 2. முக்கியக் கற்றல் கருத்து: வர்க்க வித்தியாச முற்றொருமை முறுடுகளை முழுமையாக நீக்குகிறது."),
        # Q13
        ("பகுதியை விகிதமுறு எண்ணாக்கிச் சுருக்குக: 1 / (√2 + 1)",
         ["√2 + 1", "1 − √2", "√2 − 1", "2√2"], 2,
         "தொகுதியையும் பகுதியையும் (√2 − 1)-ஆல் பெருக்கவும். (√2 − 1) / [(√2)² − 1²] = (√2 − 1) / 1 = √2 − 1. முக்கியக் கற்றல் கருத்து: √a + b வடிவப் பகுதியை விகிதமுறு எண்ணாக்க, அதன் இணை √a − b-ஆல் பெருக்கவும்."),
        # Q14
        ("0.1666… (6 மட்டும் சுழல்கிறது) என்பதைப் பின்னமாக எழுதுக.",
         ["1/5", "16/99", "1/6", "3/20"], 2,
         "x = 0.1666… என்க. எனவே 100x = 16.666…, 10x = 1.666… 90x = 15; எனவே x = 15/90 = 1/6. முக்கியக் கற்றல் கருத்து: கலப்புச் சுழல் தசமத்தில், சுழலும் பகுதியை நீக்கக் கழிக்கவும்: (எல்லா இலக்கங்கள் − சுழலாத இலக்கங்கள்) / (9-களும் 0-களும்)."),
        # Q15
        ("சுருக்குக: 0.333… + 0.666…",
         ["0.9", "0.99", "10/9", "1"], 3,
         "0.333… = 1/3, 0.666… = 2/3. 1/3 + 2/3 = 1. முக்கியக் கற்றல் கருத்து: கூட்டும் முன் சுழல் தசமங்களைப் பின்னங்களாக மாற்றவும் – துல்லியமான கூடுதல், வெட்டப்பட்ட தசமக் கூடுதலிலிருந்து வேறுபடலாம்."),
        # Q16
        ("0.454545… என்ற சுழல் தசமத்தை எளிய வடிவப் பின்னமாக எழுதுக.",
         ["5/11", "9/20", "45/100", "4/9"], 0,
         "இரண்டு இலக்கங்கள் சுழல்கின்றன; எனவே 0.4545… = 45/99. 45/99 = 5/11 (9-ஆல் வகுக்க). முக்கியக் கற்றல் கருத்து: தூய சுழல் தசமத்தில், சுழலும் தொகுப்பை அதன் இலக்க எண்ணிக்கைக்குச் சமமான 9-கள் மீது எழுதி, பின்னர் சுருக்கவும்."),
        # Q17
        ("சுருக்குக: 1 + 1/(1 + 1/(1 + 1/2))",
         ["5/3", "3/2", "13/8", "8/5"], 3,
         "உள்ளார்ந்தது: 1 + 1/2 = 3/2. அடுத்தது: 1 + 1/(3/2) = 1 + 2/3 = 5/3. வெளிப்புறம்: 1 + 1/(5/3) = 1 + 3/5 = 8/5. முக்கியக் கற்றல் கருத்து: தொடர் பின்னத்தை அடிமட்ட (உள்ளார்ந்த) நிலையிலிருந்து மேல்நோக்கிச் சுருக்கவும்."),
        # Q18
        ("சுருக்குக: (1 − 1/2)(1 − 1/3)(1 − 1/4)(1 − 1/5)",
         ["1/120", "1/4", "1/5", "4/5"], 2,
         "ஒவ்வோர் அடைப்புக்குறியும்: 1/2 × 2/3 × 3/4 × 4/5. தொகுதிகளும் பகுதிகளும் சங்கிலித் தொடராக நீங்கி, 1/5 மீதமுள்ளது. முக்கியக் கற்றல் கருத்து: அனைத்தையும் பெருக்கும் முன், ஒன்றையொன்று நீக்கும் (தொலைநோக்கி வகை) பெருக்கல்களைத் தேடவும்."),
        # Q19
        ("சுருக்குக: 1/(1×2) + 1/(2×3) + 1/(3×4) + 1/(4×5)",
         ["4/5", "5/6", "1/2", "1"], 0,
         "1/(n(n+1)) = 1/n − 1/(n+1) என்பதைப் பயன்படுத்தவும். கூடுதல் = (1 − 1/2) + (1/2 − 1/3) + (1/3 − 1/4) + (1/4 − 1/5) = 1 − 1/5 = 4/5. முக்கியக் கற்றல் கருத்து: ஒவ்வோர் உறுப்பையும் ஒரு வித்தியாசமாகப் பிரிப்பதால் நடு உறுப்புகள் நீங்குகின்றன (தொலைநோக்கிக் கூடுதல்)."),
        # Q20
        ("சுருக்குக: 0.5² ÷ 0.05",
         ["0.5", "5", "50", "0.05"], 1,
         "0.5² = 0.25. 0.25 ÷ 0.05 = 25 ÷ 5 = 5. முக்கியக் கற்றல் கருத்து: முதலில் அடுக்கை மதிப்பிடவும்; தசமங்களை வகுக்க, இரு எண்களையும் 10-இன் ஒரே அடுக்கால் பெருக்கவும்."),
        # Q21
        ("சுருக்குக: 999 × 999 + 999",
         ["998001", "999999", "999000", "1000000"], 2,
         "999-ஐப் பொதுக் காரணியாக எடுக்க: 999 × (999 + 1) = 999 × 1000 = 999000. முக்கியக் கற்றல் கருத்து: பொது உறுப்பைக் காரணிப்படுத்துவது (பங்கீட்டு விதி) பெரிய எண்களைப் பெருக்குவதைவிட விரைவானது."),
        # Q22
        ("சுருக்குக: 1.1 + 1.01 + 1.001",
         ["3.3", "3.011", "3.101", "3.111"], 3,
         "தசமப் புள்ளிகளை நேராக்க: 1.100 + 1.010 + 1.001 = 3.111. முக்கியக் கற்றல் கருத்து: கூட்டும் முன் ஒவ்வொரு தசமத்தையும் ஒரே எண்ணிக்கையிலான இடங்களுக்கு எழுதவும்."),
        # Q23
        ("சுருக்குக: (1.5³ − 0.5³) ÷ (1.5² + 1.5 × 0.5 + 0.5²)",
         ["0.5", "1.5", "2", "1"], 3,
         "a = 1.5, b = 0.5 உடன் a³ − b³ = (a − b)(a² + ab + b²) என்பதைப் பயன்படுத்தவும். பகுதி நீங்கி, a − b = 1.5 − 0.5 = 1 மீதமுள்ளது. முக்கியக் கற்றல் கருத்து: கணக்கிடும் முன், கோவையின் அமைப்பில் உள்ள நிலையான முற்றொருமைகளை அடையாளம் காணவும்."),
        # Q24
        ("சுருக்குக: 40%-இன் 250 − 3/4-இன் 80",
         ["20", "40", "60", "80"], 1,
         "250-இன் 40% = 0.4 × 250 = 100. 80-இன் 3/4 = 60. 100 − 60 = 40. முக்கியக் கற்றல் கருத்து: சதவீதங்களுக்கும் பின்னங்களுக்கும் “-இன்” என்பது பெருக்கலைக் குறிக்கிறது; கழிக்கும் முன் ஒவ்வோர் உறுப்பையும் மதிப்பிடவும்."),
        # Q25
        ("சுருக்குக: √(64.8 ÷ 0.2)",
         ["16", "20", "18", "24"], 2,
         "64.8 ÷ 0.2 = 648 ÷ 2 = 324. √324 = 18. முக்கியக் கற்றல் கருத்து: வர்க்கமூலம் காணும் முன் மூலக்குறிக்குள் உள்ள செயலை முடிக்கவும்."),
        # Q26
        ("49.97 × 20.02 ÷ 9.99-இன் தோராய மதிப்பைக் காண்க.",
         ["90", "100", "110", "1000"], 1,
         "ஒவ்வோர் எண்ணையும் வசதியான மதிப்புக்குத் தோராயமாக்க: 50 × 20 ÷ 10 = 1000 ÷ 10 = 100. முக்கியக் கற்றல் கருத்து: மதிப்பீட்டிற்கு, ஒவ்வோர் எண்ணையும் ஒருமுறை மட்டும் அருகிலுள்ள வசதியான மதிப்புக்கு முழுமையாக்கி, பின்னர் கணக்கிடவும்."),
        # Q27
        ("சுருக்குக: ∛0.008 + √0.09",
         ["0.5", "0.05", "0.23", "0.35"], 0,
         "∛0.008 = 0.2 (0.2³ = 0.008 என்பதால்). √0.09 = 0.3. 0.2 + 0.3 = 0.5. முக்கியக் கற்றல் கருத்து: சரியான முழு வர்க்கங்களாகவோ முழுக் கனங்களாகவோ உள்ள முடிவுறு தசமங்களுக்கு, தசம இடங்களைப் பொருத்தமாகக் குழுவாக்குவது (வர்க்கமூலத்துக்கு இரண்டிரண்டாக, கனமூலத்துக்கு மூன்று மூன்றாக) மூலத்தில் தசமப் புள்ளியின் இடத்தை நிர்ணயிக்க உதவுகிறது."),
        # Q28
        ("2ˣ = 32 எனில், 3^(x − 2)-இன் மதிப்பைக் காண்க.",
         ["27", "9", "81", "243"], 0,
         "32 = 2⁵; எனவே x = 5. 3^(5 − 2) = 3³ = 27. முக்கியக் கற்றல் கருத்து: தெரியாத அடுக்கைக் காண, இருபுறமும் ஒரே அடிமானத்தில் எழுதவும்."),
        # Q29
        ("சுருக்குக: 81^0.25 × 16^0.75",
         ["24", "18", "12", "36"], 0,
         "81^0.25 = 81^(1/4) = 3. 16^0.75 = 16^(3/4) = (2)³ = 8. 3 × 8 = 24. முக்கியக் கற்றல் கருத்து: தசம அடுக்குகளைப் பின்னங்களாக மாற்றவும்: 0.25 = 1/4 (நான்காம் மூலம்), 0.75 = 3/4 (நான்காம் மூலம், பின்னர் கனம்)."),
        # Q30
        ("சுருக்குக: (0.2² + 0.1²) ÷ 0.05",
         ["0.1", "10", "1", "0.5"], 2,
         "0.2² = 0.04, 0.1² = 0.01. கூடுதல் = 0.05. 0.05 ÷ 0.05 = 1. முக்கியக் கற்றல் கருத்து: அடைப்புக்குறிக்குள் உள்ள அடுக்குகளை முதலில் மதிப்பிட்டு, பின்னர் வகுக்கவும்.")
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
    out_lines.append("   ExamPro LMS - Simplification Course Seed Script (Unified Bilingual Model)")
    out_lines.append("   - 1 Course: Simplification / சுருக்குதல்")
    out_lines.append("   - 2 Assessments (Single unified assessment for both English & Tamil):")
    out_lines.append("       1. Simplification - Practice Set (simplification-practice) [55 Questions]")
    out_lines.append("          (25 Worked Examples + 30 Independent Practice in both English & Tamil)")
    out_lines.append("       2. Simplification - Graded Assessment (simplification-graded) [30 Questions]")
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
    out_lines.append("-- Clean previous Simplification courses and assessments if present")
    out_lines.append("DELETE FROM dbo.Assessments WHERE Slug IN (")
    out_lines.append("    N'simplification-practice', N'simplification-graded',")
    out_lines.append("    N'simplification-practice-en', N'simplification-graded-en',")
    out_lines.append("    N'simplification-practice-ta', N'simplification-graded-ta'")
    out_lines.append(");")
    out_lines.append("DELETE FROM dbo.Courses WHERE Slug IN (N'simplification');")
    out_lines.append("")
    out_lines.append("INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)")
    out_lines.append("VALUES (")
    out_lines.append("    N'Simplification / சுருக்குதல்',")
    out_lines.append("    N'simplification',")
    out_lines.append("    N'Comprehensive module on BODMAS, Fractions, Decimals, Surds, Indices, Complex Fractions, and Recurring Decimals for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',")
    out_lines.append("    7")
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
    out_lines.append("    (@CourseId, N'Simplification - Practice Set', N'சுருக்குதல் - பயிற்சித் தொகுப்பு', N'simplification-practice',")
    out_lines.append("     N'55 practice questions (Worked Examples + Independent Practice) with instant feedback & step-by-step solutions.',")
    out_lines.append("     N'55 பயிற்சிக் கணக்குகள் (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனடித் தீர்வுகளுடன்.',")
    out_lines.append("     N'Simplification', N'EASY', 60, 10, 55, 0, N'PRACTICE', 0, 0, 0, 1),")
    out_lines.append("    (@CourseId, N'Simplification - Graded Assessment', N'சுருக்குதல் - மதிப்பீட்டுத் தேர்வு', N'simplification-graded',")
    out_lines.append("     N'Official proctored & timed assessment on Simplification (30 Questions). Pass with 60% to master this topic.',")
    out_lines.append("     N'சுருக்குதலுக்கான அதிகாரப்பூர்வக் கண்காணிப்புடன் கூடிய தேர்வு (30 வினாக்கள்). தேர்ச்சி 60%.',")
    out_lines.append("     N'Simplification', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 2);")
    out_lines.append("")
    out_lines.append("DECLARE @pracId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'simplification-practice');")
    out_lines.append("DECLARE @gradId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'simplification-graded');")
    out_lines.append("")
    out_lines.append("-- Insert bilingual questions for @pracId (55 questions)")
    out_lines.append("INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, QuestionTextTa, OptionsJsonTa, ExplanationTa, Topic, Difficulty, OrderIndex)")
    out_lines.append("VALUES")

    p_rows = []
    for idx, (en, ta) in enumerate(zip(prac_en, prac_ta), start=1):
        q_en, opts_en, ans_en, exp_en, diff_en = en
        q_ta, opts_ta, ans_ta, exp_ta = ta
        p_rows.append(f"    (@pracId, {escape_sql(q_en)}, {escape_sql(json.dumps(opts_en, ensure_ascii=False))}, {ans_en}, {escape_sql(exp_en)}, {escape_sql(q_ta)}, {escape_sql(json.dumps(opts_ta, ensure_ascii=False))}, {escape_sql(exp_ta)}, N'Simplification', N'{diff_en}', {idx})")

    out_lines.append(",\n".join(p_rows) + ";")
    out_lines.append("")

    out_lines.append("-- Insert bilingual questions for @gradId (30 questions)")
    out_lines.append("INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, QuestionTextTa, OptionsJsonTa, ExplanationTa, Topic, Difficulty, OrderIndex)")
    out_lines.append("VALUES")

    g_rows = []
    for idx, (en, ta) in enumerate(zip(assess_en, assess_ta), start=1):
        q_en, opts_en, ans_en, exp_en, diff_en = en
        q_ta, opts_ta, ans_ta, exp_ta = ta
        g_rows.append(f"    (@gradId, {escape_sql(q_en)}, {escape_sql(json.dumps(opts_en, ensure_ascii=False))}, {ans_en}, {escape_sql(exp_en)}, {escape_sql(q_ta)}, {escape_sql(json.dumps(opts_ta, ensure_ascii=False))}, {escape_sql(exp_ta)}, N'Simplification', N'{diff_en}', {idx})")

    out_lines.append(",\n".join(g_rows) + ";")
    out_lines.append("")
    out_lines.append("COMMIT;")
    out_lines.append("PRINT 'Simplification Course seeded successfully: 1 Practice Assessment (55 Qs) and 1 Graded Assessment (30 Qs), fully bilingual (English & Tamil).';")
    out_lines.append("GO")

    out_path = os.path.join(os.path.dirname(__file__), "10_simplification_bilingual_seed.sql")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Generated {out_path} ({len(out_lines)} lines)")

if __name__ == '__main__':
    main()
