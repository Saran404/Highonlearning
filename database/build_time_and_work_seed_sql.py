# -*- coding: utf-8 -*-
"""Generates 06_time_and_work_bilingual_seed.sql containing all 85 questions from English and Tamil Time and Work PDFs."""
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
        ("A can complete a work in 10 days. Find A’s one-day work.",
         ["1/8", "1/9", "1/10", "1/12"], 2,
         "A’s one-day work = 1/10. Key Learning Point: If a person completes a work in n days, their one-day work is 1/n.", "EASY"),
        # Q2
        ("A can do a work in 12 days and B in 6 days. How long will they take working together?",
         ["3 days", "4 days", "5 days", "6 days"], 1,
         "Combined 1-day work = 1/12 + 1/6 = 1/12 + 2/12 = 3/12 = 1/4. Time = 4 days. Key Learning Point: Add individual work rates (1/time), not the times themselves, to find combined time.", "EASY"),
        # Q3
        ("If 6 men can complete a work in 15 days, how many days will 9 men take?",
         ["8", "9", "10", "12"], 2,
         "6 × 15 = 9 × x. x = 90/9 = 10 days. Key Learning Point: Men and days are inversely proportional – the product (men × days) stays constant for a fixed amount of work.", "EASY"),
        # Q4
        ("A works twice as fast as B. If B alone takes 18 days, find A’s time alone.",
         ["6", "8", "9", "12"], 2,
         "A’s time = 18 ÷ 2 = 9 days. Key Learning Point: Efficiency and time are inversely related – doubling efficiency halves the time taken.", "EASY"),
        # Q5
        ("Pipe A can fill a tank in 8 hours. Find the part of the tank filled by A in 3 hours.",
         ["1/4", "3/8", "1/2", "5/8"], 1,
         "Part filled = 3 × (1/8) = 3/8. Key Learning Point: Fraction of work completed = (time worked) ÷ (total time required).", "EASY"),
        # Q6
        ("A can do a work in 15 days and B in 20 days. They work together for 4 days, then A leaves. In how many more days will B finish the remaining work?",
         ["8", "9⅓", "10⅔", "12"], 2,
         "Combined 1-day work = 1/15 + 1/20 = 4/60 + 3/60 = 7/60. Work done in 4 days = 28/60 = 7/15; remaining = 8/15. B’s rate = 1/20 → Time = (8/15) ÷ (1/20) = 160/15 = 10⅔ days. Key Learning Point: Track work completed as a fraction before computing the remaining time for a single worker.", "MEDIUM"),
        # Q7
        ("A, B, and C can complete a work in 10, 15, and 30 days respectively. If they all work together, in how many days will the work be completed?",
         ["4", "5", "6", "7.5"], 1,
         "LCM = 30 → A = 3 units/day, B = 2 units/day, C = 1 unit/day → Total = 6 units/day. Time = 30/6 = 5 days. Key Learning Point: The LCM (unit-work) method avoids fraction-heavy computation when three or more workers are involved.", "EASY"),
        # Q8
        ("A is 25% more efficient than B. If B alone takes 25 days to complete a work, find the time taken by A and B together.",
         ["10", "11⅑", "12", "9"], 1,
         "Efficiency ratio A:B = 5:4 → Time ratio A:B = 4:5. A = 25 × 4/5 = 20 days. Combined = 1/20 + 1/25 = 5/100 + 4/100 = 9/100 → Time = 100/9 = 11⅑ days. Key Learning Point: Convert efficiency percentage into a ratio, then invert it to get the time ratio.", "MEDIUM"),
        # Q9
        ("Two pipes A and B can fill a tank in 12 and 15 hours respectively. A third pipe C can empty it in 20 hours. If all three are opened together, find the time to fill the tank.",
         ["8", "9", "10", "12"], 2,
         "Rate = 1/12 + 1/15 − 1/20. LCM = 60 → 5/60 + 4/60 − 3/60 = 6/60 = 1/10. Time = 10 hours. Key Learning Point: An outlet pipe’s rate is subtracted from, not added to, the combined fill rate.", "MEDIUM"),
        # Q10
        ("A and B undertake a work for ₹3000. A alone can do it in 8 days, B alone in 12 days. With the help of C, they finish it in 4 days. Find C’s share.",
         ["₹400", "₹500", "₹600", "₹750"], 1,
         "Combined (A+B) rate = 1/8 + 1/12 = 5/24. With C, rate needed = 1/4 = 6/24. C’s rate = 1/24. Wage ratio A:B:C = 3:2:1 → C’s share = (1/6) × 3000 = ₹500. Key Learning Point: Wages are split in the ratio of work contributed, which equals the efficiency ratio.", "MEDIUM"),
        # Q11
        ("A can complete a job in 20 days. A and B together can complete it in 12 days. Find B’s time alone.",
         ["24", "28", "30", "36"], 2,
         "B’s rate = 1/12 − 1/20 = 5/60 − 3/60 = 2/60 = 1/30. B alone = 30 days. Key Learning Point: Subtract A’s individual rate from the combined rate to isolate B’s rate.", "EASY"),
        # Q12
        ("12 men can complete a work in 18 days. After 6 days, 4 more men join. In how many total days is the work completed?",
         ["13", "14", "15", "16"], 2,
         "Total work = 12 × 18 = 216 man-days. Work done in 6 days = 72. Remaining = 144. Now 16 men → days = 144/16 = 9. Total = 6 + 9 = 15 days. Key Learning Point: Use total man-days as a constant, and recompute remaining man-days needed after any change in workforce.", "MEDIUM"),
        # Q13
        ("A and B can do a work in 18 days; B and C in 24 days; A and C in 36 days. Find the time taken if all three work together.",
         ["14", "15", "16", "18"], 2,
         "Sum of pairs = 1/18 + 1/24 + 1/36. LCM = 72 → 4/72 + 3/72 + 2/72 = 9/72 = 1/8 = 2(A+B+C). A+B+C = 1/16 → Time = 16 days. Key Learning Point: Summing all three pair-rates gives twice the combined rate of the three working together.", "MEDIUM"),
        # Q14
        ("A can do a piece of work in 24 days. He works at it for 6 days and then B finishes the remaining work in 18 days. In how long can A and B together complete the whole work?",
         ["10", "12", "14", "16"], 1,
         "A’s 6-day work = 6/24 = 1/4. Remaining = 3/4, done by B in 18 days → B’s full time = 24 days. Combined = 1/24 + 1/24 = 1/12 → Time = 12 days. Key Learning Point: Determine each person’s full individual time first, from the fraction of work they completed, before combining rates.", "MEDIUM"),
        # Q15
        ("A alone can finish a work in 12 days, which B alone can finish in 15 days. If they work on alternate days starting with A, in how many days will the work be finished?",
         ["12½", "13", "13¼", "14"], 2,
         "LCM = 60. A = 5 units/day, B = 4 units/day. In 6 cycles (12 days): 54 units done. Remaining = 6 units. Day 13 (A’s turn): A does 5 units → 59 units, remaining 1 unit. Day 14 (B’s turn): B needs ¼ day. Total = 12 + 1 + ¼ = 13¼ days. Key Learning Point: For alternate-day problems, track cumulative work per cycle, then handle the final partial day separately.", "MEDIUM"),
        # Q16
        ("A tank has an inlet pipe that fills it in 6 hours and an outlet pipe that empties it in 9 hours. If both pipes are opened together when the tank is empty, find the time to fill the tank.",
         ["15", "16", "18", "20"], 2,
         "Net rate = 1/6 − 1/9 = 3/18 − 2/18 = 1/18. Time = 18 hours. Key Learning Point: Net fill rate equals the inlet rate minus the outlet rate.", "EASY"),
        # Q17
        ("A can do a work in 20 days. B is 50% more efficient than A. If both work together, find the number of days required.",
         ["6", "7", "8", "10"], 2,
         "B’s time = 20/1.5 = 40/3 days. Combined = 1/20 + 3/40 = 2/40 + 3/40 = 5/40 = 1/8. Time = 8 days. Key Learning Point: “x% more efficient” gives an efficiency ratio; invert it to get the corresponding time ratio.", "MEDIUM"),
        # Q18
        ("15 women can complete a work in 12 days, while 10 men can complete the same work in 6 days. Find the ratio of the work efficiency of one man to one woman.",
         ["2:1", "3:1", "4:1", "5:1"], 1,
         "Total work (women) = 15 × 12 = 180 woman-days. Total work (men) = 10 × 6 = 60 man-days. 1 man-day = 3 woman-days worth → efficiency ratio man:woman = 3:1. Key Learning Point: Compare total person-days required to establish relative work rates between two groups.", "EASY"),
        # Q19
        ("A, B, and C can complete a work in 10, 15, and 30 days respectively. They start together, but A leaves after 2 days and B leaves 3 days before completion. In how many days is the work completed?",
         ["8", "9", "10", "11"], 2,
         "LCM = 30. A = 3/day, B = 2/day, C = 1/day. Let total days = x. A works 2 days = 6 units. B works (x−3) days = 2(x−3) units. C works x days = x units. 6 + 2(x−3) + x = 30 → 3x = 30 → x = 10 days. Key Learning Point: When workers join or leave partway, express each one’s contribution in terms of the unknown total days and solve algebraically.", "MEDIUM"),
        # Q20
        ("A can build a wall in 15 days, B in 20 days, and C can demolish it in 30 days. If A and B are building while C is demolishing, working together, find the time to complete the wall.",
         ["10", "12", "14", "15"], 1,
         "LCM = 60. A = 4, B = 3, C = −2 (demolishing) → Net = 5 units/day. Time = 60/5 = 12 days. Key Learning Point: A demolishing or unproductive agent acts as a negative rate in the combined work equation.", "MEDIUM"),
        # Q21
        ("A contractor employs 20 workers to complete a project in 30 days. After 10 days, he realizes only 1/4 of the work is done. How many additional workers must be employed to finish on schedule?",
         ["5", "8", "10", "12"], 2,
         "Actual pace: 20 workers × 10 days completed 1/4 of the work → total work = 800 man-days. Remaining work = 600 man-days, to be done in the remaining 20 days → workers needed = 30. Additional workers = 30 − 20 = 10. Key Learning Point: Recalculate total work based on the actual observed pace, not the originally planned pace.", "MEDIUM"),
        # Q22
        ("Two workers A and B are paid a total of ₹5000 for a job. A can do the job alone in 6 days and B in 10 days. If they work together and finish it, find B’s share.",
         ["₹1500", "₹1875", "₹2000", "₹2500"], 1,
         "Efficiency ratio A:B = (1/6):(1/10) = 5:3. B’s share = 3/8 × 5000 = ₹1875. Key Learning Point: Wage share is determined by the efficiency ratio, not the time ratio directly.", "MEDIUM"),
        # Q23
        ("A can do 1/3 of a work in 4 days and B can do 1/4 of the same work in 6 days. If they work together, in how many days will the work be completed?",
         ["6", "7", "8", "9"], 2,
         "A’s full time = 4 ÷ (1/3) = 12 days → rate = 1/12. B’s full time = 6 ÷ (1/4) = 24 days → rate = 1/24. Combined = 1/12 + 1/24 = 3/24 = 1/8 → Time = 8 days. Key Learning Point: Convert partial-work statements into each person’s full individual time before combining rates.", "EASY"),
        # Q24
        ("8 men and 4 women can complete a work in 6 days. 6 men and 8 women can complete the same work in 7 days. Find the number of days 1 man alone would take.",
         ["42", "48", "52.5", "60"], 2,
         "Let man’s rate = m, woman’s rate = w. 8m+4w = 1/6 … (i); 6m+8w = 1/7 … (ii). Solving: 10m = 4/21 → m = 2/105. 1 man’s time = 105/2 = 52.5 days. Key Learning Point: Set up two simultaneous equations in the unknown daily work rates, then solve for the required rate.", "HARD"),
        # Q25
        ("A can complete a work in ‘x’ days and B in ‘x+6’ days. Together they complete it in 4 days. Find x.",
         ["4", "5", "6", "8"], 2,
         "1/x + 1/(x+6) = 1/4 → x² − 2x − 24 = 0 → (x−6)(x+4) = 0 → x = 6 (rejecting the negative root). Key Learning Point: Form a quadratic equation from the combined work equation, and reject the extraneous (negative) root.", "MEDIUM")
    ]

    # 25 Worked Examples (Tamil)
    worked_ta = [
        # Q1
        ("A ஒரு வேலையை 10 நாட்களில் முடிக்க முடியும். A-இன் ஒரு நாள் வேலையைக் காண்க.",
         ["1/8", "1/9", "1/10", "1/12"], 2,
         "A-இன் ஒரு நாள் வேலை = 1/10. முக்கியக் கற்றல் கருத்து: ஒருவர் ஒரு வேலையை n நாட்களில் முடித்தால், அவரது ஒரு நாள் வேலை 1/n ஆகும்.", "EASY"),
        # Q2
        ("A ஒரு வேலையை 12 நாட்களிலும், B 6 நாட்களிலும் செய்ய முடியும். இருவரும் சேர்ந்து வேலை செய்தால் எவ்வளவு காலம் ஆகும்?",
         ["3 நாட்கள்", "4 நாட்கள்", "5 நாட்கள்", "6 நாட்கள்"], 1,
         "ஒருங்கிணைந்த 1 நாள் வேலை = 1/12 + 1/6 = 1/12 + 2/12 = 3/12 = 1/4. காலம் = 4 நாட்கள். முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த காலத்தைக் காண, காலங்களை அல்லாமல் தனி வேலை வீதங்களை (1/காலம்) கூட்டவும்.", "EASY"),
        # Q3
        ("6 ஆண்கள் ஒரு வேலையை 15 நாட்களில் முடிக்க முடியும் எனில், 9 ஆண்கள் எத்தனை நாட்கள் எடுப்பர்?",
         ["8", "9", "10", "12"], 2,
         "6 × 15 = 9 × x. x = 90/9 = 10 நாட்கள். முக்கியக் கற்றல் கருத்து: ஆட்களும் நாட்களும் எதிர் விகிதத்தில் உள்ளன – ஒரு நிலையான வேலைக்கு (ஆட்கள் × நாட்கள்) என்ற பெருக்கற்பலன் மாறாமல் இருக்கும்.", "EASY"),
        # Q4
        ("A, B-ஐ விட இருமடங்கு வேகமாக வேலை செய்கிறார். B தனியாக 18 நாட்கள் எடுத்தால், A தனியாக எடுக்கும் காலத்தைக் காண்க.",
         ["6", "8", "9", "12"], 2,
         "A-இன் காலம் = 18 ÷ 2 = 9 நாட்கள். முக்கியக் கற்றல் கருத்து: திறனும் காலமும் எதிர்த் தொடர்புடையவை – திறனை இருமடங்காக்கினால் காலம் பாதியாகிறது.", "EASY"),
        # Q5
        ("குழாய் A ஒரு தொட்டியை 8 மணி நேரத்தில் நிரப்ப முடியும். 3 மணி நேரத்தில் A நிரப்பும் தொட்டியின் பகுதியைக் காண்க.",
         ["1/4", "3/8", "1/2", "5/8"], 1,
         "நிரம்பிய பகுதி = 3 × (1/8) = 3/8. முக்கியக் கற்றல் கருத்து: முடிக்கப்பட்ட வேலையின் பின்னம் = (வேலை செய்த காலம்) ÷ (தேவையான மொத்தக் காலம்).", "EASY"),
        # Q6
        ("A ஒரு வேலையை 15 நாட்களிலும், B 20 நாட்களிலும் செய்ய முடியும். இருவரும் 4 நாட்கள் சேர்ந்து வேலை செய்த பின் A விலகுகிறார். மீதமுள்ள வேலையை B மேலும் எத்தனை நாட்களில் முடிப்பார்?",
         ["8", "9⅓", "10⅔", "12"], 2,
         "ஒருங்கிணைந்த 1 நாள் வேலை = 1/15 + 1/20 = 4/60 + 3/60 = 7/60. 4 நாட்களில் முடிந்த வேலை = 28/60 = 7/15; மீதம் = 8/15. B-இன் வீதம் = 1/20 → காலம் = (8/15) ÷ (1/20) = 160/15 = 10⅔ நாட்கள். முக்கியக் கற்றல் கருத்து: ஒரே பணியாளருக்கான மீதக் காலத்தைக் கணக்கிடும் முன், முடிக்கப்பட்ட வேலையைப் பின்னமாகக் கண்காணிக்கவும்.", "MEDIUM"),
        # Q7
        ("A, B, C ஆகியோர் ஒரு வேலையை முறையே 10, 15, 30 நாட்களில் முடிக்க முடியும். மூவரும் சேர்ந்து வேலை செய்தால், அவ்வேலை எத்தனை நாட்களில் முடியும்?",
         ["4", "5", "6", "7.5"], 1,
         "மீ.பொ.ம = 30 → A = 3 அலகுகள்/நாள், B = 2 அலகுகள்/நாள், C = 1 அலகு/நாள் → மொத்தம் = 6 அலகுகள்/நாள். காலம் = 30/6 = 5 நாட்கள். முக்கியக் கற்றல் கருத்து: மூன்று அல்லது அதற்கு மேற்பட்ட பணியாளர்கள் இருக்கும்போது, மீ.பொ.ம (அலகு-வேலை) முறை பின்னக் கணக்கீடுகளைத் தவிர்க்கிறது.", "EASY"),
        # Q8
        ("A, B-ஐ விட 25% அதிகத் திறன் உடையவர். B தனியாக ஒரு வேலையை 25 நாட்களில் முடித்தால், A மற்றும் B சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["10", "11⅑", "12", "9"], 1,
         "திறன் விகிதம் A:B = 5:4 → கால விகிதம் A:B = 4:5. A = 25 × 4/5 = 20 நாட்கள். ஒருங்கிணைந்தது = 1/20 + 1/25 = 5/100 + 4/100 = 9/100 → காலம் = 100/9 = 11⅑ நாட்கள். முக்கியக் கற்றல் கருத்து: திறன் சதவீதத்தை விகிதமாக மாற்றி, பின்னர் அதைத் தலைகீழாக்கிக் கால விகிதத்தைப் பெறவும்.", "MEDIUM"),
        # Q9
        ("A மற்றும் B என்ற இரண்டு குழாய்கள் ஒரு தொட்டியை முறையே 12 மற்றும் 15 மணி நேரத்தில் நிரப்ப முடியும். மூன்றாவது குழாய் C அதை 20 மணி நேரத்தில் காலி செய்ய முடியும். மூன்றும் ஒரே நேரத்தில் திறக்கப்பட்டால், தொட்டி நிரம்ப ஆகும் காலத்தைக் காண்க.",
         ["8", "9", "10", "12"], 2,
         "வீதம் = 1/12 + 1/15 − 1/20. மீ.பொ.ம = 60 → 5/60 + 4/60 − 3/60 = 6/60 = 1/10. காலம் = 10 மணி நேரம். முக்கியக் கற்றல் கருத்து: வெளியேற்றும் குழாயின் வீதம் ஒருங்கிணைந்த நிரப்பும் வீதத்துடன் கூட்டப்படுவதில்லை; கழிக்கப்படுகிறது.", "MEDIUM"),
        # Q10
        ("A மற்றும் B ஒரு வேலையை ₹3000-க்கு ஏற்கின்றனர். A தனியாக அதை 8 நாட்களிலும், B தனியாக 12 நாட்களிலும் செய்ய முடியும். C-இன் உதவியுடன் அவர்கள் 4 நாட்களில் முடிக்கின்றனர். C-இன் பங்கைக் காண்க.",
         ["₹400", "₹500", "₹600", "₹750"], 1,
         "ஒருங்கிணைந்த (A+B) வீதம் = 1/8 + 1/12 = 5/24. C-உடன் தேவையான வீதம் = 1/4 = 6/24. C-இன் வீதம் = 1/24. கூலி விகிதம் A:B:C = 3:2:1 → C-இன் பங்கு = (1/6) × 3000 = ₹500. முக்கியக் கற்றல் கருத்து: கூலி செய்த வேலையின் விகிதத்தில் பகிரப்படுகிறது; இது திறன் விகிதத்திற்குச் சமம்.", "MEDIUM"),
        # Q11
        ("A ஒரு வேலையை 20 நாட்களில் முடிக்க முடியும். A மற்றும் B சேர்ந்து 12 நாட்களில் முடிக்க முடியும். B தனியாக எடுக்கும் காலத்தைக் காண்க.",
         ["24", "28", "30", "36"], 2,
         "B-இன் வீதம் = 1/12 − 1/20 = 5/60 − 3/60 = 2/60 = 1/30. B தனியாக = 30 நாட்கள். முக்கியக் கற்றல் கருத்து: B-இன் வீதத்தைத் தனியாகப் பெற, ஒருங்கிணைந்த வீதத்திலிருந்து A-இன் தனி வீதத்தைக் கழிக்கவும்.", "EASY"),
        # Q12
        ("12 ஆண்கள் ஒரு வேலையை 18 நாட்களில் முடிக்க முடியும். 6 நாட்களுக்குப் பின் மேலும் 4 ஆண்கள் சேர்கின்றனர். மொத்தம் எத்தனை நாட்களில் வேலை முடியும்?",
         ["13", "14", "15", "16"], 2,
         "மொத்த வேலை = 12 × 18 = 216 ஆள்-நாட்கள். 6 நாட்களில் முடிந்த வேலை = 72. மீதம் = 144. இப்போது 16 ஆண்கள் → நாட்கள் = 144/16 = 9. மொத்தம் = 6 + 9 = 15 நாட்கள். முக்கியக் கற்றல் கருத்து: மொத்த ஆள்-நாட்களை மாறிலியாகக் கொண்டு, பணியாளர் எண்ணிக்கை மாறிய பின் தேவையான மீத ஆள்-நாட்களை மீண்டும் கணக்கிடவும்.", "MEDIUM"),
        # Q13
        ("A மற்றும் B ஒரு வேலையை 18 நாட்களிலும்; B மற்றும் C 24 நாட்களிலும்; A மற்றும் C 36 நாட்களிலும் செய்ய முடியும். மூவரும் சேர்ந்து வேலை செய்தால் எடுக்கும் காலத்தைக் காண்க.",
         ["14", "15", "16", "18"], 2,
         "இணைகளின் கூடுதல் = 1/18 + 1/24 + 1/36. மீ.பொ.ம = 72 → 4/72 + 3/72 + 2/72 = 9/72 = 1/8 = 2(A+B+C). A+B+C = 1/16 → காலம் = 16 நாட்கள். முக்கியக் கற்றல் கருத்து: மூன்று இணை வீதங்களையும் கூட்டினால், மூவரும் சேர்ந்து செய்யும் ஒருங்கிணைந்த வீதத்தின் இருமடங்கு கிடைக்கும்.", "MEDIUM"),
        # Q14
        ("A ஒரு வேலையை 24 நாட்களில் செய்ய முடியும். அவர் 6 நாட்கள் வேலை செய்த பின், மீதமுள்ள வேலையை B 18 நாட்களில் முடிக்கிறார். A மற்றும் B சேர்ந்து முழு வேலையை எவ்வளவு காலத்தில் முடிப்பர்?",
         ["10", "12", "14", "16"], 1,
         "A-இன் 6 நாள் வேலை = 6/24 = 1/4. மீதம் = 3/4; இதை B 18 நாட்களில் செய்கிறார் → B-இன் முழுக் காலம் = 24 நாட்கள். ஒருங்கிணைந்தது = 1/24 + 1/24 = 1/12 → காலம் = 12 நாட்கள். முக்கியக் கற்றல் கருத்து: வீதங்களை இணைக்கும் முன், ஒவ்வொருவரும் முடித்த வேலைப் பின்னத்திலிருந்து அவரது முழுத் தனிக் காலத்தை முதலில் கண்டறியவும்.", "MEDIUM"),
        # Q15
        ("A தனியாக ஒரு வேலையை 12 நாட்களில் முடிக்க முடியும்; B தனியாக அதை 15 நாட்களில் முடிக்க முடியும். A-இலிருந்து தொடங்கி அவர்கள் மாற்று நாட்களில் வேலை செய்தால், வேலை எத்தனை நாட்களில் முடியும்?",
         ["12½", "13", "13¼", "14"], 2,
         "மீ.பொ.ம = 60. A = 5 அலகுகள்/நாள், B = 4 அலகுகள்/நாள். 6 சுழற்சிகளில் (12 நாட்கள்): 54 அலகுகள் முடிந்தன. மீதம் = 6 அலகுகள். 13-ஆம் நாள் (A-இன் முறை): A 5 அலகுகள் செய்கிறார் → 59 அலகுகள், மீதம் 1 அலகு. 14-ஆம் நாள் (B-இன் முறை): B-க்கு ¼ நாள் தேவை. மொத்தம் = 12 + 1 + ¼ = 13¼ நாட்கள். முக்கியக் கற்றல் கருத்து: மாற்று நாள் கணக்குகளில், ஒவ்வொரு சுழற்சிக்குமான கூட்டு வேலையைக் கண்காணித்து, இறுதிப் பகுதி நாளைத் தனியாகக் கையாளவும்.", "MEDIUM"),
        # Q16
        ("ஒரு தொட்டியில் அதை 6 மணி நேரத்தில் நிரப்பும் ஒரு நிரப்பும் குழாயும், 9 மணி நேரத்தில் காலி செய்யும் ஒரு வெளியேற்றும் குழாயும் உள்ளன. தொட்டி காலியாக இருக்கும்போது இரண்டு குழாய்களும் திறக்கப்பட்டால், தொட்டி நிரம்ப ஆகும் காலத்தைக் காண்க.",
         ["15", "16", "18", "20"], 2,
         "நிகர வீதம் = 1/6 − 1/9 = 3/18 − 2/18 = 1/18. காலம் = 18 மணி நேரம். முக்கியக் கற்றல் கருத்து: நிகர நிரப்பும் வீதம் = நிரப்பும் வீதம் − வெளியேற்றும் வீதம்.", "EASY"),
        # Q17
        ("A ஒரு வேலையை 20 நாட்களில் செய்ய முடியும். B, A-ஐ விட 50% அதிகத் திறன் உடையவர். இருவரும் சேர்ந்து வேலை செய்தால், தேவையான நாட்களின் எண்ணிக்கையைக் காண்க.",
         ["6", "7", "8", "10"], 2,
         "B-இன் காலம் = 20/1.5 = 40/3 நாட்கள். ஒருங்கிணைந்தது = 1/20 + 3/40 = 2/40 + 3/40 = 5/40 = 1/8. காலம் = 8 நாட்கள். முக்கியக் கற்றல் கருத்து: “x% அதிகத் திறன்” என்பது ஒரு திறன் விகிதத்தைத் தருகிறது; அதைத் தலைகீழாக்கித் தொடர்புடைய கால விகிதத்தைப் பெறவும்.", "MEDIUM"),
        # Q18
        ("15 பெண்கள் ஒரு வேலையை 12 நாட்களில் முடிக்க முடியும்; 10 ஆண்கள் அதே வேலையை 6 நாட்களில் முடிக்க முடியும். ஓர் ஆணுக்கும் ஒரு பெண்ணுக்கும் இடையிலான வேலைத்திறன் விகிதத்தைக் காண்க.",
         ["2:1", "3:1", "4:1", "5:1"], 1,
         "மொத்த வேலை (பெண்கள்) = 15 × 12 = 180 பெண்-நாட்கள். மொத்த வேலை (ஆண்கள்) = 10 × 6 = 60 ஆண்-நாட்கள். 1 ஆண்-நாள் = 3 பெண்-நாட்களுக்குச் சமம் → திறன் விகிதம் ஆண்:பெண் = 3:1. முக்கியக் கற்றல் கருத்து: இரு குழுக்களுக்கிடையிலான சார்பு வேலை வீதங்களை அறிய, தேவைப்படும் மொத்த ஆள்-நாட்களை ஒப்பிடவும்.", "EASY"),
        # Q19
        ("A, B, C ஆகியோர் ஒரு வேலையை முறையே 10, 15, 30 நாட்களில் முடிக்க முடியும். மூவரும் சேர்ந்து தொடங்குகின்றனர்; ஆனால் A 2 நாட்களுக்குப் பின் விலகுகிறார், B வேலை முடிவதற்கு 3 நாட்களுக்கு முன் விலகுகிறார். வேலை எத்தனை நாட்களில் முடியும்?",
         ["8", "9", "10", "11"], 2,
         "மீ.பொ.ம = 30. A = 3/நாள், B = 2/நாள், C = 1/நாள். மொத்த நாட்கள் = x என்க. A 2 நாட்கள் வேலை செய்கிறார் = 6 அலகுகள். B (x−3) நாட்கள் வேலை செய்கிறார் = 2(x−3) அலகுகள். C x நாட்கள் வேலை செய்கிறார் = x அலகுகள். 6 + 2(x−3) + x = 30 → 3x = 30 → x = 10 நாட்கள். முக்கியக் கற்றல் கருத்து: பணியாளர்கள் இடையில் சேரும்போது அல்லது விலகும்போது, ஒவ்வொருவரின் பங்களிப்பையும் தெரியாத மொத்த நாட்களின் அடிப்படையில் வெளிப்படுத்தி இயற்கணித முறையில் தீர்க்கவும்.", "MEDIUM"),
        # Q20
        ("A ஒரு சுவரை 15 நாட்களிலும், B 20 நாட்களிலும் கட்ட முடியும்; C அதை 30 நாட்களில் இடிக்க முடியும். A மற்றும் B கட்டிக்கொண்டிருக்கும்போது C இடித்துக்கொண்டிருந்தால், மூவரும் சேர்ந்து சுவரைக் கட்டி முடிக்க ஆகும் காலத்தைக் காண்க.",
         ["10", "12", "14", "15"], 1,
         "மீ.பொ.ம = 60. A = 4, B = 3, C = −2 (இடித்தல்) → நிகரம் = 5 அலகுகள்/நாள். காலம் = 60/5 = 12 நாட்கள். முக்கியக் கற்றல் கருத்து: இடிக்கும் அல்லது பயனற்ற செயல்பாட்டாளர், ஒருங்கிணைந்த வேலைச் சமன்பாட்டில் எதிர்மறை வீதமாகச் செயல்படுகிறார்.", "MEDIUM"),
        # Q21
        ("ஓர் ஒப்பந்ததாரர் ஒரு திட்டத்தை 30 நாட்களில் முடிக்க 20 பணியாளர்களை அமர்த்துகிறார். 10 நாட்களுக்குப் பின், வேலையில் 1/4 பகுதி மட்டுமே முடிந்திருப்பதை அவர் உணர்கிறார். திட்டமிட்டபடி முடிக்க மேலும் எத்தனை பணியாளர்களை அமர்த்த வேண்டும்?",
         ["5", "8", "10", "12"], 2,
         "உண்மையான வேகம்: 20 பணியாளர்கள் × 10 நாட்கள் வேலையில் 1/4 பகுதியை முடித்தனர் → மொத்த வேலை = 800 ஆள்-நாட்கள். மீத வேலை = 600 ஆள்-நாட்கள்; இதை மீதமுள்ள 20 நாட்களில் முடிக்க வேண்டும் → தேவையான பணியாளர்கள் = 30. கூடுதல் பணியாளர்கள் = 30 − 20 = 10. முக்கியக் கற்றல் கருத்து: மொத்த வேலையை முதலில் திட்டமிட்ட வேகத்தின் அடிப்படையில் அல்லாமல், உண்மையில் காணப்பட்ட வேகத்தின் அடிப்படையில் மீண்டும் கணக்கிடவும்.", "MEDIUM"),
        # Q22
        ("A மற்றும் B என்ற இரண்டு பணியாளர்களுக்கு ஒரு வேலைக்கு மொத்தம் ₹5000 வழங்கப்படுகிறது. A தனியாக அவ்வேலையை 6 நாட்களிலும், B 10 நாட்களிலும் செய்ய முடியும். இருவரும் சேர்ந்து வேலையை முடித்தால், B-இன் பங்கைக் காண்க.",
         ["₹1500", "₹1875", "₹2000", "₹2500"], 1,
         "திறன் விகிதம் A:B = (1/6):(1/10) = 5:3. B-இன் பங்கு = 3/8 × 5000 = ₹1875. முக்கியக் கற்றல் கருத்து: கூலிப் பங்கு கால விகிதத்தால் நேரடியாக அல்லாமல், திறன் விகிதத்தால் தீர்மானிக்கப்படுகிறது.", "MEDIUM"),
        # Q23
        ("A ஒரு வேலையின் 1/3 பகுதியை 4 நாட்களிலும், B அதே வேலையின் 1/4 பகுதியை 6 நாட்களிலும் செய்ய முடியும். இருவரும் சேர்ந்து வேலை செய்தால், வேலை எத்தனை நாட்களில் முடியும்?",
         ["6", "7", "8", "9"], 2,
         "A-இன் முழுக் காலம் = 4 ÷ (1/3) = 12 நாட்கள் → வீதம் = 1/12. B-இன் முழுக் காலம் = 6 ÷ (1/4) = 24 நாட்கள் → வீதம் = 1/24. ஒருங்கிணைந்தது = 1/12 + 1/24 = 3/24 = 1/8 → காலம் = 8 நாட்கள். முக்கியக் கற்றல் கருத்து: வீதங்களை இணைக்கும் முன், பகுதி-வேலைக் கூற்றுகளை ஒவ்வொருவரின் முழுத் தனிக் காலமாக மாற்றவும்.", "EASY"),
        # Q24
        ("8 ஆண்களும் 4 பெண்களும் ஒரு வேலையை 6 நாட்களில் முடிக்க முடியும். 6 ஆண்களும் 8 பெண்களும் அதே வேலையை 7 நாட்களில் முடிக்க முடியும். 1 ஆண் தனியாக எடுக்கும் நாட்களின் எண்ணிக்கையைக் காண்க.",
         ["42", "48", "52.5", "60"], 2,
         "ஆணின் வீதம் = m, பெண்ணின் வீதம் = w என்க. 8m+4w = 1/6 … (i); 6m+8w = 1/7 … (ii). தீர்க்க: 10m = 4/21 → m = 2/105. 1 ஆணின் காலம் = 105/2 = 52.5 நாட்கள். முக்கியக் கற்றல் கருத்து: தெரியாத தினசரி வேலை வீதங்களில் இரண்டு ஒருங்கமைச் சமன்பாடுகளை அமைத்து, தேவையான வீதத்தைக் காணவும்.", "HARD"),
        # Q25
        ("A ஒரு வேலையை ‘x’ நாட்களிலும், B ‘x+6’ நாட்களிலும் முடிக்க முடியும். இருவரும் சேர்ந்து 4 நாட்களில் முடிக்கின்றனர். x-ஐக் காண்க.",
         ["4", "5", "6", "8"], 2,
         "1/x + 1/(x+6) = 1/4 → x² − 2x − 24 = 0 → (x−6)(x+4) = 0 → x = 6 (எதிர்மறை மூலத்தை நீக்கி). முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த வேலைச் சமன்பாட்டிலிருந்து ஓர் இருபடிச் சமன்பாட்டை அமைத்து, பொருந்தாத (எதிர்மறை) மூலத்தை நீக்கவும்.", "MEDIUM")
    ]

    # 30 Independent Practice (English)
    indep_en = [
        # Q1
        ("A can complete a work in 9 days. Find A’s one-day work.",
         ["1/7", "1/8", "1/9", "1/10"], 2,
         "A’s one-day work = 1/9. Key Learning Point: One-day work = 1/(number of days to complete).", "EASY"),
        # Q2
        ("A can do a job in 10 days, B in 15 days. Find the time taken together.",
         ["5", "6", "7", "8"], 1,
         "Combined = 1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6 → 6 days. Key Learning Point: Add individual rates, not the times themselves.", "EASY"),
        # Q3
        ("If 8 men finish a work in 20 days, how many days for 10 men?",
         ["14", "15", "16", "18"], 2,
         "8 × 20 = 10 × x → x = 16 days. Key Learning Point: Men and days are inversely proportional for a fixed quantity of work.", "EASY"),
        # Q4
        ("A is thrice as fast as B. If B takes 24 days alone, find A’s time.",
         ["6", "8", "10", "12"], 1,
         "A’s time = 24/3 = 8 days. Key Learning Point: Higher efficiency means proportionally lower time, based on the given multiple.", "EASY"),
        # Q5
        ("Pipe A fills a tank in 5 hours. What fraction is filled in 2 hours?",
         ["1/3", "2/5", "1/2", "3/5"], 1,
         "Fraction filled = 2/5. Key Learning Point: Fraction filled = (time worked) ÷ (total time to fill).", "EASY"),
        # Q6
        ("A can do a work in 14 days and B in 21 days. Find their combined 1-day work.",
         ["1/12", "5/42", "1/7", "3/35"], 1,
         "Combined = 1/14 + 1/21 = 3/42 + 2/42 = 5/42. Key Learning Point: Add the reciprocals of individual times to get the combined work rate.", "EASY"),
        # Q7
        ("A and B can do a work in 12 and 16 days respectively. They work together for 3 days, then A leaves. Find how many more days B needs to finish.",
         ["7", "8", "9", "10"], 2,
         "Combined rate = 1/12 + 1/16 = 7/48. Work done in 3 days = 21/48 = 7/16. Remaining = 9/16. B’s rate = 1/16 → Time = 9 days. Key Learning Point: Subtract the work already done (as a fraction) before computing the remaining time.", "MEDIUM"),
        # Q8
        ("A, B, and C can complete a work in 8, 12, and 24 days respectively. Find the time taken if all work together.",
         ["3", "4", "5", "6"], 1,
         "LCM = 24 → A=3, B=2, C=1 → total = 6 units/day → Time = 24/6 = 4 days. Key Learning Point: The LCM (unit-work) method is the fastest approach for multi-person combined work problems.", "EASY"),
        # Q9
        ("A is 20% more efficient than B. B alone takes 24 days. Find the combined time.",
         ["10", "10 10/11", "11", "12"], 1,
         "Efficiency ratio A:B = 6:5 → Time ratio A:B = 5:6 → A = 20 days. Combined = 1/20 + 1/24 = 11/120 → Time = 120/11 = 10 10/11 days. Key Learning Point: Convert efficiency percentage to a ratio before finding individual and combined times.", "MEDIUM"),
        # Q10
        ("Pipes A and B fill a tank in 10 and 15 hours; pipe C empties it in 12 hours. Find the time to fill the tank if all three are opened together.",
         ["10", "11", "12", "15"], 2,
         "LCM = 60 → 6/60 + 4/60 − 5/60 = 5/60 = 1/12. Time = 12 hours. Key Learning Point: Net rate equals the sum of inlet rates minus the outlet rate.", "MEDIUM"),
        # Q11
        ("A and B undertake a work for ₹4200. A alone takes 10 days, B alone 15 days. With C’s help they finish in 5 days. Find C’s share.",
         ["₹600", "₹700", "₹800", "₹900"], 1,
         "Combined (A+B) = 1/10 + 1/15 = 1/6. With C, rate needed = 1/5. C’s rate = 1/5 − 1/6 = 1/30. Wage ratio A:B:C = 3:2:1 → C’s share = (1/6) × 4200 = ₹700. Key Learning Point: C’s rate is found by subtracting the (A+B) rate from the rate needed to finish in the given time.", "MEDIUM"),
        # Q12
        ("A can complete a job in 16 days. A and B together take 10 days. Find B’s time alone.",
         ["24", "25", "26⅔", "28"], 2,
         "B’s rate = 1/10 − 1/16 = 3/80 → B’s time = 80/3 = 26⅔ days. Key Learning Point: Isolate B’s rate by subtracting A’s rate from the combined rate.", "MEDIUM"),
        # Q13
        ("10 men complete a work in 15 days. After 5 days, 5 more men join. Find the total number of days to finish.",
         ["10", "11⅔", "12", "13"], 1,
         "Total work = 150 man-days. Done in 5 days = 50. Remaining = 100. Now 15 men → days = 100/15 = 6⅔. Total = 5 + 6⅔ = 11⅔ days. Key Learning Point: Track remaining man-days needed after the workforce changes.", "MEDIUM"),
        # Q14
        ("A and B do a work in 20 days; B and C in 24 days; A and C in 30 days. Find the time for all three together.",
         ["14", "15", "16", "18"], 2,
         "Sum = 1/20 + 1/24 + 1/30 = 15/120 = 1/8 = 2(A+B+C) → A+B+C = 1/16. Time = 16 days. Key Learning Point: Sum all three pair-rates, then divide by two, to get the combined rate of all three.", "MEDIUM"),
        # Q15
        ("A can do a work in 18 days. He works 6 days, then B finishes the rest in 24 days. Find the time for A and B together.",
         ["10", "12", "14", "15"], 1,
         "A’s 6-day work = 1/3. Remaining = 2/3, done by B in 24 days → B’s full time = 36 days. Combined = 1/18 + 1/36 = 1/12 → Time = 12 days. Key Learning Point: Determine B’s full time from the fraction of work they actually completed.", "MEDIUM"),
        # Q16
        ("A and B alternate days starting with A. A alone takes 10 days, B alone 15 days. Find the total time to finish.",
         ["11", "12", "13", "14"], 1,
         "LCM = 30. A=3/day, B=2/day. Cycle of 2 days = 5 units. 6 cycles (12 days) = 30 units — exactly complete. Time = 12 days. Key Learning Point: For alternate-day problems, check whether the cycles divide evenly into the total work before handling a remainder.", "MEDIUM"),
        # Q17
        ("A tank’s inlet fills it in 8 hours; outlet empties it in 12 hours. Both opened together — find the time to fill.",
         ["20", "22", "24", "28"], 2,
         "Net rate = 1/8 − 1/12 = 1/24. Time = 24 hours. Key Learning Point: Net fill rate equals the inlet rate minus the outlet rate.", "EASY"),
        # Q18
        ("A can do a work in 24 days. B is 20% more efficient. Find the combined time.",
         ["10", "10 10/11", "11", "12"], 1,
         "Efficiency ratio A:B = 5:6 → B’s time = 20 days. Combined = 1/24 + 1/20 = 11/120 → Time = 10 10/11 days. Key Learning Point: Convert efficiency percentage to a ratio before combining rates.", "MEDIUM"),
        # Q19
        ("12 women complete a work in 10 days; 8 men complete it in 6 days. Find the man: woman efficiency ratio.",
         ["2:1", "5:2", "3:1", "7:2"], 1,
         "Total work (women) = 120 woman-days. Total work (men) = 48 man-days. 1 man-day = 2.5 woman-days → ratio = 5:2. Key Learning Point: Compare total person-days to establish relative work rates between two groups.", "EASY"),
        # Q20
        ("A, B, C take 8, 12, and 24 days respectively. A leaves after 2 days; B leaves 3 days before completion. Find total days.",
         ["6", "7", "8", "9"], 2,
         "LCM = 24. A=3/day, B=2/day, C=1/day. Let total = x. 6 + 2(x−3) + x = 24 → 3x = 24 → x = 8 days. Key Learning Point: Express each worker’s contribution in terms of the unknown total days and solve algebraically.", "MEDIUM"),
        # Q21
        ("A builds a wall in 8 days, B in 12 days; C demolishes it in 24 days. All work together — find the time to complete.",
         ["5", "6", "7", "8"], 1,
         "LCM = 24. A=3, B=2, C=−1 → Net = 4 units/day. Time = 24/4 = 6 days. Key Learning Point: A demolishing agent’s rate is subtracted from the combined building rate.", "EASY"),
        # Q22
        ("A contractor hires 25 workers for a 40-day project. After 15 days, only 1/3 is complete. How many additional workers are needed to finish on time?",
         ["3", "5", "7", "10"], 1,
         "Worker-days used = 375 for 1/3 work → total work = 1125 man-days. Remaining = 750 man-days in 25 days. Workers needed = 750/25 = 30 → additional = 5. Key Learning Point: Recalculate total work based on the actual observed pace, not the target pace.", "MEDIUM"),
        # Q23
        ("A and B are paid ₹6000 total. A alone takes 8 days, B alone 12 days. Find B’s share if they work together.",
         ["₹2000", "₹2200", "₹2400", "₹2600"], 2,
         "Efficiency ratio A:B = 3:2 → B’s share = 2/5 × 6000 = ₹2400. Key Learning Point: Wage split follows the efficiency ratio, not the time ratio directly.", "MEDIUM"),
        # Q24
        ("A does 1/4 of a work in 3 days; B does 1/5 of the work in 4 days. Find the time together.",
         ["6.5", "7", "7.5", "8"], 2,
         "A’s full time = 12 days → rate = 1/12. B’s full time = 20 days → rate = 1/20. Combined = 1/12 + 1/20 = 5/60 + 3/60 = 8/60 = 2/15 → Time = 15/2 = 7.5 days. Key Learning Point: Convert partial-work statements into full individual times before combining.", "MEDIUM"),
        # Q25
        ("6 men and 3 women complete a work in 8 days; 4 men and 9 women complete it in 8 days as well. Find the ratio of 1 man’s to 1 woman’s work rate.",
         ["2:1", "3:1", "4:1", "5:1"], 1,
         "6m+3w = 1/8; 4m+9w = 1/8 → solving simultaneously gives m:w = 3:1. Key Learning Point: Set up two equations from the two given scenarios and solve them simultaneously.", "HARD"),
        # Q26
        ("A takes ‘x’ days, B takes ‘x+5’ days; together they take 6 days. Find x.",
         ["8", "9", "10", "12"], 2,
         "1/x + 1/(x+5) = 1/6 → x² − 7x − 30 = 0 → (x−10)(x+3) = 0 → x = 10. Key Learning Point: Form a quadratic from the combined work equation and reject the extraneous negative root.", "MEDIUM"),
        # Q27
        ("A can finish a work in 15 days working 8 hours/day. How many days will he take working 6 hours/day?",
         ["18", "20", "22", "24"], 1,
         "Total work = 15 × 8 = 120 hours. At 6 hours/day → 120/6 = 20 days. Key Learning Point: Convert to total working hours, then divide by the new daily hours.", "EASY"),
        # Q28
        ("Two taps can fill a cistern in 12 and 18 minutes. A drainage pipe can empty it in 9 minutes. If all three are opened together, find whether the cistern fills or empties, and in how much time.",
         ["Empties, 18 min", "Fills, 24 min", "Fills, 36 min", "Empties, 36 min"], 2,
         "Net rate = 1/12 + 1/18 − 1/9 = 3/36 + 2/36 − 4/36 = 1/36 (positive, so it fills). Time = 36 minutes. Key Learning Point: Check the sign of the net rate first – positive means it fills, negative means it empties.", "MEDIUM"),
        # Q29
        ("A, B, and C together can complete a work in 6 days. A alone takes 12 days and B alone takes 18 days. Find C’s time alone.",
         ["30", "33", "36", "40"], 2,
         "A+B = 1/12 + 1/18 = 5/36. C’s rate = 1/6 − 5/36 = 1/36. C alone = 36 days. Key Learning Point: Subtract the sum of the known workers’ rates from the combined rate to isolate the unknown worker’s rate.", "MEDIUM"),
        # Q30
        ("15 workers can complete a task in 24 days. After 8 days, 5 workers leave. Find the total number of days to complete the task.",
         ["28", "30", "32", "34"], 2,
         "Total work = 360 worker-days. Done in 8 days = 120. Remaining = 240. Now 10 workers → 24 days. Total = 8 + 24 = 32 days. Key Learning Point: Recalculate remaining work-days needed after the workforce decreases.", "MEDIUM")
    ]

    # 30 Independent Practice (Tamil)
    indep_ta = [
        # Q1
        ("A ஒரு வேலையை 9 நாட்களில் முடிக்க முடியும். A-இன் ஒரு நாள் வேலையைக் காண்க.",
         ["1/7", "1/8", "1/9", "1/10"], 2,
         "A-இன் ஒரு நாள் வேலை = 1/9. முக்கியக் கற்றல் கருத்து: ஒரு நாள் வேலை = 1/(முடிக்க எடுக்கும் நாட்கள்).", "EASY"),
        # Q2
        ("A ஒரு வேலையை 10 நாட்களிலும், B 15 நாட்களிலும் செய்ய முடியும். இருவரும் சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["5", "6", "7", "8"], 1,
         "ஒருங்கிணைந்தது = 1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6 → 6 நாட்கள். முக்கியக் கற்றல் கருத்து: காலங்களை அல்லாமல் தனி வீதங்களைக் கூட்டவும்.", "EASY"),
        # Q3
        ("8 ஆண்கள் ஒரு வேலையை 20 நாட்களில் முடித்தால், 10 ஆண்களுக்கு எத்தனை நாட்கள் ஆகும்?",
         ["14", "15", "16", "18"], 2,
         "8 × 20 = 10 × x → x = 16 நாட்கள். முக்கியக் கற்றல் கருத்து: ஒரு நிலையான வேலைக்கு ஆட்களும் நாட்களும் எதிர் விகிதத்தில் உள்ளன.", "EASY"),
        # Q4
        ("A, B-ஐ விட மும்மடங்கு வேகமானவர். B தனியாக 24 நாட்கள் எடுத்தால், A-இன் காலத்தைக் காண்க.",
         ["6", "8", "10", "12"], 1,
         "A-இன் காலம் = 24/3 = 8 நாட்கள். முக்கியக் கற்றல் கருத்து: கொடுக்கப்பட்ட மடங்கின் அடிப்படையில், அதிகத் திறன் என்பது விகிதாசாரமாகக் குறைந்த காலம் ஆகும்.", "EASY"),
        # Q5
        ("குழாய் A ஒரு தொட்டியை 5 மணி நேரத்தில் நிரப்புகிறது. 2 மணி நேரத்தில் எப்பகுதி நிரம்பும்?",
         ["1/3", "2/5", "1/2", "3/5"], 1,
         "நிரம்பிய பின்னம் = 2/5. முக்கியக் கற்றல் கருத்து: நிரம்பிய பின்னம் = (வேலை செய்த காலம்) ÷ (நிரப்பத் தேவையான மொத்தக் காலம்).", "EASY"),
        # Q6
        ("A ஒரு வேலையை 14 நாட்களிலும், B 21 நாட்களிலும் செய்ய முடியும். அவர்களின் ஒருங்கிணைந்த 1 நாள் வேலையைக் காண்க.",
         ["1/12", "5/42", "1/7", "3/35"], 1,
         "ஒருங்கிணைந்தது = 1/14 + 1/21 = 3/42 + 2/42 = 5/42. முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த வேலை வீதத்தைப் பெற, தனிக் காலங்களின் தலைகீழிகளைக் கூட்டவும்.", "EASY"),
        # Q7
        ("A மற்றும் B ஒரு வேலையை முறையே 12 மற்றும் 16 நாட்களில் செய்ய முடியும். இருவரும் 3 நாட்கள் சேர்ந்து வேலை செய்த பின் A விலகுகிறார். வேலையை முடிக்க B-க்கு மேலும் எத்தனை நாட்கள் தேவை?",
         ["7", "8", "9", "10"], 2,
         "ஒருங்கிணைந்த வீதம் = 1/12 + 1/16 = 7/48. 3 நாட்களில் முடிந்த வேலை = 21/48 = 7/16. மீதம் = 9/16. B-இன் வீதம் = 1/16 → காலம் = 9 நாட்கள். முக்கியக் கற்றல் கருத்து: மீதக் காலத்தைக் கணக்கிடும் முன், ஏற்கெனவே முடிந்த வேலையை (பின்னமாக) கழிக்கவும்.", "MEDIUM"),
        # Q8
        ("A, B, C ஆகியோர் ஒரு வேலையை முறையே 8, 12, 24 நாட்களில் முடிக்க முடியும். அனைவரும் சேர்ந்து வேலை செய்தால் எடுக்கும் காலத்தைக் காண்க.",
         ["3", "4", "5", "6"], 1,
         "மீ.பொ.ம = 24 → A=3, B=2, C=1 → மொத்தம் = 6 அலகுகள்/நாள் → காலம் = 24/6 = 4 நாட்கள். முக்கியக் கற்றல் கருத்து: பலர் சேர்ந்து செய்யும் வேலைக் கணக்குகளுக்கு மீ.பொ.ம (அலகு-வேலை) முறையே விரைவான அணுகுமுறையாகும்.", "EASY"),
        # Q9
        ("A, B-ஐ விட 20% அதிகத் திறன் உடையவர். B தனியாக 24 நாட்கள் எடுக்கிறார். ஒருங்கிணைந்த காலத்தைக் காண்க.",
         ["10", "10 10/11", "11", "12"], 1,
         "திறன் விகிதம் A:B = 6:5 → கால விகிதம் A:B = 5:6 → A = 20 நாட்கள். ஒருங்கிணைந்தது = 1/20 + 1/24 = 11/120 → காலம் = 120/11 = 10 10/11 நாட்கள். முக்கியக் கற்றல் கருத்து: தனி மற்றும் ஒருங்கிணைந்த காலங்களைக் காணும் முன், திறன் சதவீதத்தை விகிதமாக மாற்றவும்.", "MEDIUM"),
        # Q10
        ("குழாய்கள் A மற்றும் B ஒரு தொட்டியை 10 மற்றும் 15 மணி நேரத்தில் நிரப்புகின்றன; குழாய் C அதை 12 மணி நேரத்தில் காலி செய்கிறது. மூன்றும் ஒரே நேரத்தில் திறக்கப்பட்டால், தொட்டி நிரம்ப ஆகும் காலத்தைக் காண்க.",
         ["10", "11", "12", "15"], 2,
         "மீ.பொ.ம = 60 → 6/60 + 4/60 − 5/60 = 5/60 = 1/12. காலம் = 12 மணி நேரம். முக்கியக் கற்றல் கருத்து: நிகர வீதம் = நிரப்பும் வீதங்களின் கூடுதல் − வெளியேற்றும் வீதம்.", "MEDIUM"),
        # Q11
        ("A மற்றும் B ஒரு வேலையை ₹4200-க்கு ஏற்கின்றனர். A தனியாக 10 நாட்களும், B தனியாக 15 நாட்களும் எடுக்கின்றனர். C-இன் உதவியுடன் அவர்கள் 5 நாட்களில் முடிக்கின்றனர். C-இன் பங்கைக் காண்க.",
         ["₹600", "₹700", "₹800", "₹900"], 1,
         "ஒருங்கிணைந்த (A+B) = 1/10 + 1/15 = 1/6. C-உடன் தேவையான வீதம் = 1/5. C-இன் வீதம் = 1/5 − 1/6 = 1/30. கூலி விகிதம் A:B:C = 3:2:1 → C-இன் பங்கு = (1/6) × 4200 = ₹700. முக்கியக் கற்றல் கருத்து: கொடுக்கப்பட்ட காலத்தில் முடிக்கத் தேவையான வீதத்திலிருந்து (A+B) வீதத்தைக் கழித்து C-இன் வீதம் கண்டறியப்படுகிறது.", "MEDIUM"),
        # Q12
        ("A ஒரு வேலையை 16 நாட்களில் முடிக்க முடியும். A மற்றும் B சேர்ந்து 10 நாட்கள் எடுக்கின்றனர். B தனியாக எடுக்கும் காலத்தைக் காண்க.",
         ["24", "25", "26⅔", "28"], 2,
         "B-இன் வீதம் = 1/10 − 1/16 = 3/80 → B-இன் காலம் = 80/3 = 26⅔ நாட்கள். முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த வீதத்திலிருந்து A-இன் வீதத்தைக் கழித்து B-இன் வீதத்தைத் தனியாகப் பெறவும்.", "MEDIUM"),
        # Q13
        ("10 ஆண்கள் ஒரு வேலையை 15 நாட்களில் முடிக்கின்றனர். 5 நாட்களுக்குப் பின் மேலும் 5 ஆண்கள் சேர்கின்றனர். வேலையை முடிக்க ஆகும் மொத்த நாட்களைக் காண்க.",
         ["10", "11⅔", "12", "13"], 1,
         "மொத்த வேலை = 150 ஆள்-நாட்கள். 5 நாட்களில் முடிந்தது = 50. மீதம் = 100. இப்போது 15 ஆண்கள் → நாட்கள் = 100/15 = 6⅔. மொத்தம் = 5 + 6⅔ = 11⅔ நாட்கள். முக்கியக் கற்றல் கருத்து: பணியாளர் எண்ணிக்கை மாறிய பின் தேவையான மீத ஆள்-நாட்களைக் கண்காணிக்கவும்.", "MEDIUM"),
        # Q14
        ("A மற்றும் B ஒரு வேலையை 20 நாட்களிலும்; B மற்றும் C 24 நாட்களிலும்; A மற்றும் C 30 நாட்களிலும் செய்கின்றனர். மூவரும் சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["14", "15", "16", "18"], 2,
         "கூடுதல் = 1/20 + 1/24 + 1/30 = 15/120 = 1/8 = 2(A+B+C) → A+B+C = 1/16. காலம் = 16 நாட்கள். முக்கியக் கற்றல் கருத்து: மூன்று இணை வீதங்களையும் கூட்டி, இரண்டால் வகுத்து மூவரின் ஒருங்கிணைந்த வீதத்தைப் பெறவும்.", "MEDIUM"),
        # Q15
        ("A ஒரு வேலையை 18 நாட்களில் செய்ய முடியும். அவர் 6 நாட்கள் வேலை செய்த பின், மீதமுள்ளதை B 24 நாட்களில் முடிக்கிறார். A மற்றும் B சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["10", "12", "14", "15"], 1,
         "A-இன் 6 நாள் வேலை = 1/3. மீதம் = 2/3; இதை B 24 நாட்களில் செய்கிறார் → B-இன் முழுக் காலம் = 36 நாட்கள். ஒருங்கிணைந்தது = 1/18 + 1/36 = 1/12 → காலம் = 12 நாட்கள். முக்கியக் கற்றல் கருத்து: B உண்மையில் முடித்த வேலைப் பின்னத்திலிருந்து B-இன் முழுக் காலத்தைக் கண்டறியவும்.", "MEDIUM"),
        # Q16
        ("A-இலிருந்து தொடங்கி A மற்றும் B மாற்று நாட்களில் வேலை செய்கின்றனர். A தனியாக 10 நாட்களும், B தனியாக 15 நாட்களும் எடுக்கின்றனர். வேலையை முடிக்க ஆகும் மொத்தக் காலத்தைக் காண்க.",
         ["11", "12", "13", "14"], 1,
         "மீ.பொ.ம = 30. A=3/நாள், B=2/நாள். 2 நாள் சுழற்சி = 5 அலகுகள். 6 சுழற்சிகள் (12 நாட்கள்) = 30 அலகுகள் — சரியாக முடிகிறது. காலம் = 12 நாட்கள். முக்கியக் கற்றல் கருத்து: மாற்று நாள் கணக்குகளில், மீதியைக் கையாளும் முன், சுழற்சிகள் மொத்த வேலையைச் சரியாக வகுக்கின்றனவா எனச் சரிபார்க்கவும்.", "MEDIUM"),
        # Q17
        ("ஒரு தொட்டியின் நிரப்பும் குழாய் அதை 8 மணி நேரத்தில் நிரப்புகிறது; வெளியேற்றும் குழாய் 12 மணி நேரத்தில் காலி செய்கிறது. இரண்டும் ஒரே நேரத்தில் திறக்கப்பட்டால் — தொட்டி நிரம்ப ஆகும் காலத்தைக் காண்க.",
         ["20", "22", "24", "28"], 2,
         "நிகர வீதம் = 1/8 − 1/12 = 1/24. காலம் = 24 மணி நேரம். முக்கியக் கற்றல் கருத்து: நிகர நிரப்பும் வீதம் = நிரப்பும் வீதம் − வெளியேற்றும் வீதம்.", "EASY"),
        # Q18
        ("A ஒரு வேலையை 24 நாட்களில் செய்ய முடியும். B, 20% அதிகத் திறன் உடையவர். ஒருங்கிணைந்த காலத்தைக் காண்க.",
         ["10", "10 10/11", "11", "12"], 1,
         "திறன் விகிதம் A:B = 5:6 → B-இன் காலம் = 20 நாட்கள். ஒருங்கிணைந்தது = 1/24 + 1/20 = 11/120 → காலம் = 10 10/11 நாட்கள். முக்கியக் கற்றல் கருத்து: வீதங்களை இணைக்கும் முன், திறன் சதவீதத்தை விகிதமாக மாற்றவும்.", "MEDIUM"),
        # Q19
        ("12 பெண்கள் ஒரு வேலையை 10 நாட்களில் முடிக்கின்றனர்; 8 ஆண்கள் அதை 6 நாட்களில் முடிக்கின்றனர். ஆண் : பெண் திறன் விகிதத்தைக் காண்க.",
         ["2:1", "5:2", "3:1", "7:2"], 1,
         "மொத்த வேலை (பெண்கள்) = 120 பெண்-நாட்கள். மொத்த வேலை (ஆண்கள்) = 48 ஆண்-நாட்கள். 1 ஆண்-நாள் = 2.5 பெண்-நாட்கள் → விகிதம் = 5:2. முக்கியக் கற்றல் கருத்து: இரு குழுக்களுக்கிடையிலான சார்பு வேலை வீதங்களை அறிய, மொத்த ஆள்-நாட்களை ஒப்பிடவும்.", "EASY"),
        # Q20
        ("A, B, C ஆகியோர் முறையே 8, 12, 24 நாட்கள் எடுக்கின்றனர். A 2 நாட்களுக்குப் பின் விலகுகிறார்; B வேலை முடிவதற்கு 3 நாட்களுக்கு முன் விலகுகிறார். மொத்த நாட்களைக் காண்க.",
         ["6", "7", "8", "9"], 2,
         "மீ.பொ.ம = 24. A=3/நாள், B=2/நாள், C=1/நாள். மொத்தம் = x என்க. 6 + 2(x−3) + x = 24 → 3x = 24 → x = 8 நாட்கள். முக்கியக் கற்றல் கருத்து: ஒவ்வொரு பணியாளரின் பங்களிப்பையும் தெரியாத மொத்த நாட்களின் அடிப்படையில் வெளிப்படுத்தி இயற்கணித முறையில் தீர்க்கவும்.", "MEDIUM"),
        # Q21
        ("A ஒரு சுவரை 8 நாட்களிலும், B 12 நாட்களிலும் கட்டுகின்றனர்; C அதை 24 நாட்களில் இடிக்கிறார். அனைவரும் சேர்ந்து வேலை செய்தால் — சுவர் முடிய ஆகும் காலத்தைக் காண்க.",
         ["5", "6", "7", "8"], 1,
         "மீ.பொ.ம = 24. A=3, B=2, C=−1 → நிகரம் = 4 அலகுகள்/நாள். காலம் = 24/4 = 6 நாட்கள். முக்கியக் கற்றல் கருத்து: இடிப்பவரின் வீதம் ஒருங்கிணைந்த கட்டும் வீதத்திலிருந்து கழிக்கப்படுகிறது.", "EASY"),
        # Q22
        ("ஓர் ஒப்பந்ததாரர் 40 நாள் திட்டத்திற்கு 25 பணியாளர்களை அமர்த்துகிறார். 15 நாட்களுக்குப் பின், 1/3 பகுதி மட்டுமே முடிந்துள்ளது. குறித்த காலத்தில் முடிக்க மேலும் எத்தனை பணியாளர்கள் தேவை?",
         ["3", "5", "7", "10"], 1,
         "பயன்படுத்திய பணியாளர்-நாட்கள் = 1/3 வேலைக்கு 375 → மொத்த வேலை = 1125 ஆள்-நாட்கள். மீதம் = 25 நாட்களில் 750 ஆள்-நாட்கள். தேவையான பணியாளர்கள் = 750/25 = 30 → கூடுதல் = 5. முக்கியக் கற்றல் கருத்து: மொத்த வேலையை இலக்கு வேகத்தின் அடிப்படையில் அல்லாமல், உண்மையில் காணப்பட்ட வேகத்தின் அடிப்படையில் மீண்டும் கணக்கிடவும்.", "MEDIUM"),
        # Q23
        ("A மற்றும் B-க்கு மொத்தம் ₹6000 வழங்கப்படுகிறது. A தனியாக 8 நாட்களும், B தனியாக 12 நாட்களும் எடுக்கின்றனர். இருவரும் சேர்ந்து வேலை செய்தால் B-இன் பங்கைக் காண்க.",
         ["₹2000", "₹2200", "₹2400", "₹2600"], 2,
         "திறன் விகிதம் A:B = 3:2 → B-இன் பங்கு = 2/5 × 6000 = ₹2400. முக்கியக் கற்றல் கருத்து: கூலிப் பகிர்வு கால விகிதத்தை நேரடியாக அல்லாமல், திறன் விகிதத்தைப் பின்பற்றுகிறது.", "MEDIUM"),
        # Q24
        ("A ஒரு வேலையின் 1/4 பகுதியை 3 நாட்களில் செய்கிறார்; B அவ்வேலையின் 1/5 பகுதியை 4 நாட்களில் செய்கிறார். இருவரும் சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["6.5", "7", "7.5", "8"], 2,
         "A-இன் முழுக் காலம் = 12 நாட்கள் → வீதம் = 1/12. B-இன் முழுக் காலம் = 20 நாட்கள் → வீதம் = 1/20. ஒருங்கிணைந்தது = 1/12 + 1/20 = 5/60 + 3/60 = 8/60 = 2/15 → காலம் = 15/2 = 7.5 நாட்கள். முக்கியக் கற்றல் கருத்து: இணைக்கும் முன், பகுதி-வேலைக் கூற்றுகளை முழுத் தனிக் காலங்களாக மாற்றவும்.", "MEDIUM"),
        # Q25
        ("6 ஆண்களும் 3 பெண்களும் ஒரு வேலையை 8 நாட்களில் முடிக்கின்றனர்; 4 ஆண்களும் 9 பெண்களும் அதையும் 8 நாட்களிலேயே முடிக்கின்றனர். 1 ஆணின் வேலை வீதத்திற்கும் 1 பெண்ணின் வேலை வீதத்திற்கும் இடையிலான விகிதத்தைக் காண்க.",
         ["2:1", "3:1", "4:1", "5:1"], 1,
         "6m+3w = 1/8; 4m+9w = 1/8 → ஒருங்கமைத் தீர்வு m:w = 3:1 எனத் தருகிறது. முக்கியக் கற்றல் கருத்து: கொடுக்கப்பட்ட இரண்டு சூழல்களிலிருந்து இரண்டு சமன்பாடுகளை அமைத்து அவற்றை ஒருங்கே தீர்க்கவும்.", "HARD"),
        # Q26
        ("A ‘x’ நாட்களும், B ‘x+5’ நாட்களும் எடுக்கின்றனர்; இருவரும் சேர்ந்து 6 நாட்கள் எடுக்கின்றனர். x-ஐக் காண்க.",
         ["8", "9", "10", "12"], 2,
         "1/x + 1/(x+5) = 1/6 → x² − 7x − 30 = 0 → (x−10)(x+3) = 0 → x = 10. முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த வேலைச் சமன்பாட்டிலிருந்து ஓர் இருபடிச் சமன்பாட்டை அமைத்து, பொருந்தாத எதிர்மறை மூலத்தை நீக்கவும்.", "MEDIUM"),
        # Q27
        ("A நாளொன்றுக்கு 8 மணி நேரம் வேலை செய்து ஒரு வேலையை 15 நாட்களில் முடிக்க முடியும். நாளொன்றுக்கு 6 மணி நேரம் வேலை செய்தால் அவர் எத்தனை நாட்கள் எடுப்பார்?",
         ["18", "20", "22", "24"], 1,
         "மொத்த வேலை = 15 × 8 = 120 மணி நேரம். நாளொன்றுக்கு 6 மணி நேரம் → 120/6 = 20 நாட்கள். முக்கியக் கற்றல் கருத்து: மொத்த வேலை மணி நேரமாக மாற்றி, பின்னர் புதிய தினசரி மணி நேரத்தால் வகுக்கவும்.", "EASY"),
        # Q28
        ("இரண்டு குழாய்கள் ஒரு நீர்த்தொட்டியை 12 மற்றும் 18 நிமிடங்களில் நிரப்ப முடியும். ஒரு வடிகால் குழாய் அதை 9 நிமிடங்களில் காலி செய்ய முடியும். மூன்றும் ஒரே நேரத்தில் திறக்கப்பட்டால், தொட்டி நிரம்புமா அல்லது காலியாகுமா, எவ்வளவு நேரத்தில் எனக் காண்க.",
         ["காலியாகும், 18 நிமி", "நிரம்பும், 24 நிமி", "நிரம்பும், 36 நிமி", "காலியாகும், 36 நிமி"], 2,
         "நிகர வீதம் = 1/12 + 1/18 − 1/9 = 3/36 + 2/36 − 4/36 = 1/36 (நேர்மறை, எனவே நிரம்பும்). காலம் = 36 நிமிடங்கள். முக்கியக் கற்றல் கருத்து: முதலில் நிகர வீதத்தின் குறியைச் சரிபார்க்கவும் – நேர்மறை என்றால் நிரம்பும், எதிர்மறை என்றால் காலியாகும்.", "MEDIUM"),
        # Q29
        ("A, B, C சேர்ந்து ஒரு வேலையை 6 நாட்களில் முடிக்க முடியும். A தனியாக 12 நாட்களும், B தனியாக 18 நாட்களும் எடுக்கின்றனர். C தனியாக எடுக்கும் காலத்தைக் காண்க.",
         ["30", "33", "36", "40"], 2,
         "A+B = 1/12 + 1/18 = 5/36. C-இன் வீதம் = 1/6 − 5/36 = 1/36. C தனியாக = 36 நாட்கள். முக்கியக் கற்றல் கருத்து: தெரியாத பணியாளரின் வீதத்தைத் தனியாகப் பெற, ஒருங்கிணைந்த வீதத்திலிருந்து தெரிந்த பணியாளர்களின் வீதங்களின் கூடுதலைக் கழிக்கவும்.", "MEDIUM"),
        # Q30
        ("15 பணியாளர்கள் ஒரு பணியை 24 நாட்களில் முடிக்க முடியும். 8 நாட்களுக்குப் பின் 5 பணியாளர்கள் விலகுகின்றனர். பணியை முடிக்க ஆகும் மொத்த நாட்களைக் காண்க.",
         ["28", "30", "32", "34"], 2,
         "மொத்த வேலை = 360 பணியாளர்-நாட்கள். 8 நாட்களில் முடிந்தது = 120. மீதம் = 240. இப்போது 10 பணியாளர்கள் → 24 நாட்கள். மொத்தம் = 8 + 24 = 32 நாட்கள். முக்கியக் கற்றல் கருத்து: பணியாளர் எண்ணிக்கை குறைந்த பின் தேவையான மீத வேலை-நாட்களை மீண்டும் கணக்கிடவும்.", "MEDIUM")
    ]

    # 30 Graded Assessment (English)
    graded_en = [
        # Q1
        ("A can complete a work in 11 days. Find A’s one-day work.",
         ["1/9", "1/10", "1/11", "1/12"], 2,
         "A's one-day work = 1/11. Key Learning Point: If a person completes a work in n days, their one-day work is 1/n.", "EASY"),
        # Q2
        ("A can do a job in 8 days, B in 24 days. Find their combined time.",
         ["5", "6", "7", "8"], 1,
         "Combined 1-day work = 1/8 + 1/24 = 3/24 + 1/24 = 4/24 = 1/6. Time = 6 days. Key Learning Point: Add individual work rates (1/time), not the times themselves.", "EASY"),
        # Q3
        ("If 5 machines produce a batch in 24 days, how many days for 8 machines?",
         ["12", "14", "15", "16"], 2,
         "5 × 24 = 8 × x. x = 120/8 = 15 days. Key Learning Point: Machines and days are inversely proportional — the product (machines × days) stays constant.", "EASY"),
        # Q4
        ("A is four times as fast as B. B alone takes 20 days. Find A’s time.",
         ["4", "5", "6", "8"], 1,
         "A's time = 20 ÷ 4 = 5 days. Key Learning Point: If A is k times as fast as B, A takes 1/k of B's time.", "EASY"),
        # Q5
        ("Pipe A fills a tank in 6 hours. What fraction is filled in 4 hours?",
         ["1/2", "3/5", "2/3", "3/4"], 2,
         "Fraction filled = 4 × (1/6) = 4/6 = 2/3. Key Learning Point: Fraction of work completed = (time worked) ÷ (total time required).", "EASY"),
        # Q6
        ("A can do a work in 16 days and B in 24 days. Find their combined 1-day work.",
         ["1/12", "5/48", "1/8", "7/48"], 1,
         "Combined 1-day work = 1/16 + 1/24 = 3/48 + 2/48 = 5/48. Key Learning Point: Use the LCM of the denominators to add the work rates quickly.", "EASY"),
        # Q7
        ("A and B can do a work in 10 and 14 days. They work together for 2 days, then A leaves. Find the time B needs for the rest.",
         ["8.5", "9", "9.2", "10"], 2,
         "Combined 1-day work = 1/10 + 1/14 = 7/70 + 5/70 = 12/70 = 6/35. Work done in 2 days = 12/35; remaining = 23/35. B's rate = 1/14 → Time = (23/35) ÷ (1/14) = (23 × 14)/35 = 9.2 days. Key Learning Point: Find the fraction of work already completed before computing the remaining time for a single worker.", "MEDIUM"),
        # Q8
        ("A, B, C complete a work in 6, 9, and 18 days. Find the time together.",
         ["2", "3", "4", "5"], 1,
         "LCM = 18 → A = 3 units/day, B = 2 units/day, C = 1 unit/day → Total = 6 units/day. Time = 18/6 = 3 days. Key Learning Point: The LCM (unit-work) method avoids fraction-heavy arithmetic with three or more workers.", "EASY"),
        # Q9
        ("A is 25% more efficient than B. B alone takes 20 days. Find their combined time.",
         ["8", "8⁸⁄₉", "9", "10"], 1,
         "Efficiency ratio A:B = 5:4 → Time ratio A:B = 4:5. A's time = 20 × 4/5 = 16 days. Combined = 1/16 + 1/20 = 5/80 + 4/80 = 9/80 → Time = 80/9 = 8⁸⁄₉ days. Key Learning Point: Convert the efficiency percentage into a ratio, then invert it to get the time ratio.", "MEDIUM"),
        # Q10
        ("Pipes A and B fill a tank in 8 and 12 hours; pipe C empties it in 24 hours. All three opened together — find the fill time.",
         ["5", "6", "7", "8"], 1,
         "LCM = 24 → Rate = 3/24 + 2/24 − 1/24 = 4/24 = 1/6. Time = 6 hours. Key Learning Point: An outlet pipe's rate is subtracted from the combined fill rate.", "MEDIUM"),
        # Q11
        ("A and B undertake a job for ₹3600. A alone takes 9 days, B alone 12 days. With C’s help they finish in 4 days. Find C’s share.",
         ["₹700", "₹750", "₹800", "₹900"], 2,
         "Combined (A+B) rate = 1/9 + 1/12 = 4/36 + 3/36 = 7/36. With C, rate needed = 1/4 = 9/36. C's rate = 9/36 − 7/36 = 2/36. Wage ratio A:B:C = 4:3:2 → C's share = (2/9) × 3600 = ₹800. Key Learning Point: Wages are shared in the ratio of work contributed, which equals the efficiency ratio when all work the same number of days.", "MEDIUM"),
        # Q12
        ("A can complete a job in 18 days. A and B together take 11 days. Find B’s time alone.",
         ["26", "27", "28 2/7", "30"], 2,
         "B's rate = 1/11 − 1/18 = 18/198 − 11/198 = 7/198. B's time = 198/7 = 28 2/7 days. Key Learning Point: Subtract A's rate from the combined rate to isolate B's rate.", "MEDIUM"),
        # Q13
        ("8 men complete a work in 20 days. After 4 days, 4 more men join. Find total days to finish.",
         ["13", "14", "14⅔", "15"], 2,
         "Total work = 8 × 20 = 160 man-days. Work done in 4 days = 32. Remaining = 128. Now 12 men → days = 128/12 = 10⅔. Total = 4 + 10⅔ = 14⅔ days. Key Learning Point: Keep total man-days constant and recompute the remaining man-days after the workforce changes.", "MEDIUM"),
        # Q14
        ("A and B do a work in 20 days; B and C in 30 days; A and C in 60 days. Find the time for all three together.",
         ["15", "18", "20", "24"], 2,
         "Sum of pairs = 1/20 + 1/30 + 1/60. LCM = 60 → 3/60 + 2/60 + 1/60 = 6/60 = 1/10 = 2(A+B+C). A+B+C = 1/20 → Time = 20 days. Key Learning Point: Adding all three pair-rates gives twice the combined rate of the three working together.", "MEDIUM"),
        # Q15
        ("A can do a work in 21 days. He works 7 days, then B finishes the rest in 21 days. Find the time for A and B together.",
         ["12", "12.6", "13", "14"], 1,
         "A's 7-day work = 7/21 = 1/3. Remaining = 2/3, done by B in 21 days → B's full time = 21 ÷ (2/3) = 31.5 days. Combined = 1/21 + 1/31.5 = 3/63 + 2/63 = 5/63 → Time = 63/5 = 12.6 days. Key Learning Point: Find each person's full individual time from the fraction of work they completed, then combine the rates.", "MEDIUM"),
        # Q16
        ("A and B alternate days, starting with A. A alone takes 12 days, B alone 18 days. Find total time.",
         ["13⅔", "14", "14⅓", "15"], 2,
         "LCM = 36. A = 3 units/day, B = 2 units/day. Cycle of 2 days = 5 units. 7 cycles (14 days) = 35 units. Remaining = 1 unit. Day 15 (A's turn): A needs 1/3 day. Total = 14 + ⅓ = 14⅓ days. Key Learning Point: For alternate-day problems, complete as many full cycles as possible, then handle the final partial day.", "MEDIUM"),
        # Q17
        ("An inlet pipe fills a tank in 10 hours; an outlet empties it in 15 hours. Both open together — find the fill time.",
         ["24", "28", "30", "36"], 2,
         "Net rate = 1/10 − 1/15 = 3/30 − 2/30 = 1/30. Time = 30 hours. Key Learning Point: Net fill rate = inlet rate − outlet rate.", "EASY"),
        # Q18
        ("A can do a work in 30 days. B is 25% more efficient. Find the combined time.",
         ["12", "13⅓", "14", "15"], 1,
         "Efficiency ratio A:B = 4:5 → B's time = 30 × 4/5 = 24 days. Combined = 1/30 + 1/24 = 4/120 + 5/120 = 9/120 → Time = 120/9 = 13⅓ days. Key Learning Point: \"x% more efficient\" gives an efficiency ratio; invert it to get the time ratio.", "MEDIUM"),
        # Q19
        ("10 women complete a work in 18 days; 6 men complete it in 10 days. Find the man:woman efficiency ratio.",
         ["2:1", "2.5:1", "3:1", "4:1"], 2,
         "Total work (women) = 10 × 18 = 180 woman-days. Total work (men) = 6 × 10 = 60 man-days. 1 man-day = 180/60 = 3 woman-days → efficiency ratio man:woman = 3:1. Key Learning Point: Compare total person-days required to find the relative work rates of two groups.", "EASY"),
        # Q20
        ("A, B, C take 12, 18, and 36 days. A leaves after 4 days; B leaves 3 days before completion. Find total days.",
         ["8", "9", "10", "12"], 2,
         "LCM = 36. A = 3/day, B = 2/day, C = 1/day. Let total days = x. A works 4 days = 12 units. B works (x−3) days = 2(x−3) units. C works x days = x units. 12 + 2(x−3) + x = 36 → 3x + 6 = 36 → x = 10 days. Key Learning Point: Express each worker's contribution in terms of the unknown total days and solve algebraically.", "MEDIUM"),
        # Q21
        ("A builds a wall in 10 days, B in 15 days; C demolishes it in 15 days. All work together — find the completion time.",
         ["8", "9", "10", "12"], 2,
         "LCM = 30. A = 3, B = 2, C = −2 (demolishing) → Net = 3 units/day. Time = 30/3 = 10 days. Key Learning Point: A demolishing agent acts as a negative rate in the combined work equation.", "MEDIUM"),
        # Q22
        ("A contractor hires 30 workers for a 25-day project. After 10 days, only 1/3 is done. How many additional workers are needed?",
         ["5", "8", "10", "12"], 2,
         "30 workers × 10 days = 300 man-days completed 1/3 of the work → total work = 900 man-days. Remaining work = 600 man-days, to be done in the remaining 15 days → workers needed = 600/15 = 40. Additional workers = 40 − 30 = 10. Key Learning Point: Recalculate total work from the actual observed pace, not the planned pace.", "MEDIUM"),
        # Q23
        ("A and B are paid ₹7200 total. A alone takes 6 days, B alone 9 days. Find B’s share.",
         ["2400", "2600", "2880", "3000"], 2,
         "Efficiency ratio A:B = (1/6):(1/9) = 3:2. B's share = (2/5) × 7200 = ₹2,880. Key Learning Point: Wage share follows the efficiency ratio (1/time), not the time ratio directly.", "MEDIUM"),
        # Q24
        ("A does 2/5 of a work in 8 days; B does 1/3 of the work in 10 days. Find the time taken if they work together.",
         ["10", "11", "12", "15"], 2,
         "A's full time = 8 ÷ (2/5) = 20 days → rate = 1/20. B's full time = 10 ÷ (1/3) = 30 days → rate = 1/30. Combined = 1/20 + 1/30 = 3/60 + 2/60 = 5/60 = 1/12 → Time = 12 days. Key Learning Point: Full time = (days taken) ÷ (fraction of work done). Convert each partial-work statement before combining rates.", "MEDIUM"),
        # Q25
        ("5 men and 4 women complete a work in 9 days; 3 men and 6 women complete it in 10 days. Find the man:woman work-rate ratio.",
         ["5:3", "7:4", "8:5", "9:5"], 2,
         "Let man's rate = m, woman's rate = w. 5m + 4w = 1/9 and 3m + 6w = 1/10. Total work is the same: 9(5m + 4w) = 10(3m + 6w) ⟹ 45m + 36w = 30m + 60w ⟹ 15m = 24w. m : w = 24 : 15 = 8 : 5. Key Learning Point: Equate the total work in the two scenarios (group rate × days) to relate the individual rates.", "HARD"),
        # Q26
        ("A takes ‘x’ days, B takes ‘x+8’ days; together they take 7½ days. Find x.",
         ["10", "11", "12", "14"], 2,
         "1/x + 1/(x+8) = 2/15. 15(2x + 8) = 2x(x + 8) ⟹ 30x + 120 = 2x² + 16x ⟹ x² − 7x − 60 = 0. (x − 12)(x + 5) = 0 → x = 12 (rejecting the negative root). Check: 1/12 + 1/20 = 5/60 + 3/60 = 8/60 = 2/15 ✓. Key Learning Point: Form a quadratic from the combined work equation, reject the negative root, and verify the answer.", "MEDIUM"),
        # Q27
        ("A finishes a work in 12 days working 10 hours/day. How many days at 8 hours/day?",
         ["12", "14", "15", "18"], 2,
         "Total work = 12 × 10 = 120 hours. At 8 hours/day → 120/8 = 15 days. Key Learning Point: Convert to total working hours, then divide by the new daily hours.", "EASY"),
        # Q28
        ("Two taps fill a cistern in 10 and 15 minutes; a drain empties it in 6 minutes. All three opened together — find whether it fills/empties and in how much time.",
         ["Fills, 30 min", "Empties, 30 min", "Stays constant (net rate zero)", "Fills, 36 min"], 2,
         "Net rate = 1/10 + 1/15 − 1/6. LCM = 30 → 3/30 + 2/30 − 5/30 = 0. Net rate is zero, so the water level stays constant. Key Learning Point: Check the sign of the net rate first: positive means it fills, negative means it empties, zero means no change.", "MEDIUM"),
        # Q29
        ("A, B, C together finish a work in 4 days. A alone takes 9 days, B alone takes 12 days. Find C’s time alone.",
         ["15", "16", "18", "20"], 2,
         "A+B = 1/9 + 1/12 = 4/36 + 3/36 = 7/36. C's rate = 1/4 − 7/36 = 9/36 − 7/36 = 2/36 = 1/18. C alone = 18 days. Key Learning Point: Subtract the known workers' rates from the combined rate to isolate the unknown worker's rate.", "MEDIUM"),
        # Q30
        ("20 workers complete a task in 18 days. After 6 days, 4 workers leave. Find the total days to complete.",
         ["18", "20", "21", "24"], 2,
         "Total work = 20 × 18 = 360 worker-days. Done in 6 days = 120. Remaining = 240. Now 16 workers → 240/16 = 15 days. Total = 6 + 15 = 21 days. Key Learning Point: Recalculate the remaining worker-days after the workforce decreases.", "MEDIUM")
    ]

    # 30 Graded Assessment (Tamil)
    graded_ta = [
        # Q1
        ("A ஒரு வேலையை 11 நாட்களில் முடிக்க முடியும். A-இன் ஒரு நாள் வேலையைக் காண்க.",
         ["1/9", "1/10", "1/11", "1/12"], 2,
         "A-இன் ஒரு நாள் வேலை = 1/11. முக்கியக் கற்றல் கருத்து: ஒருவர் ஒரு வேலையை n நாட்களில் முடித்தால், அவரது ஒரு நாள் வேலை 1/n ஆகும்.", "EASY"),
        # Q2
        ("A ஒரு வேலையை 8 நாட்களிலும், B 24 நாட்களிலும் செய்ய முடியும். அவர்களின் ஒருங்கிணைந்த காலத்தைக் காண்க.",
         ["5", "6", "7", "8"], 1,
         "ஒருங்கிணைந்த 1 நாள் வேலை = 1/8 + 1/24 = 3/24 + 1/24 = 4/24 = 1/6. காலம் = 6 நாட்கள். முக்கியக் கற்றல் கருத்து: காலங்களை அல்லாமல் தனி வேலை வீதங்களை (1/காலம்) கூட்டவும்.", "EASY"),
        # Q3
        ("5 இயந்திரங்கள் ஒரு தொகுப்பை 24 நாட்களில் உற்பத்தி செய்தால், 8 இயந்திரங்களுக்கு எத்தனை நாட்கள் ஆகும்?",
         ["12", "14", "15", "16"], 2,
         "5 × 24 = 8 × x. x = 120/8 = 15 நாட்கள். முக்கியக் கற்றல் கருத்து: இயந்திரங்களும் நாட்களும் எதிர் விகிதத்தில் உள்ளன — (இயந்திரங்கள் × நாட்கள்) என்ற பெருக்கற்பலன் மாறாது.", "EASY"),
        # Q4
        ("A, B-ஐ விட நான்கு மடங்கு வேகமானவர். B தனியாக 20 நாட்கள் எடுக்கிறார். A-இன் காலத்தைக் காண்க.",
         ["4", "5", "6", "8"], 1,
         "A-இன் காலம் = 20 ÷ 4 = 5 நாட்கள். முக்கியக் கற்றல் கருத்து: A, B-ஐ விட k மடங்கு வேகமானவர் எனில், A, B-இன் காலத்தில் 1/k பங்கு எடுத்துக்கொள்வார்.", "EASY"),
        # Q5
        ("குழாய் A ஒரு தொட்டியை 6 மணி நேரத்தில் நிரப்புகிறது. 4 மணி நேரத்தில் எப்பகுதி நிரம்பும்?",
         ["1/2", "3/5", "2/3", "3/4"], 2,
         "நிரம்பிய பின்னம் = 4 × (1/6) = 4/6 = 2/3. முக்கியக் கற்றல் கருத்து: முடிக்கப்பட்ட வேலையின் பின்னம் = (வேலை செய்த காலம்) ÷ (தேவையான மொத்தக் காலம்).", "EASY"),
        # Q6
        ("A ஒரு வேலையை 16 நாட்களிலும், B 24 நாட்களிலும் செய்ய முடியும். அவர்களின் ஒருங்கிணைந்த 1 நாள் வேலையைக் காண்க.",
         ["1/12", "5/48", "1/8", "7/48"], 1,
         "ஒருங்கிணைந்த 1 நாள் வேலை = 1/16 + 1/24 = 3/48 + 2/48 = 5/48. முக்கியக் கற்றல் கருத்து: வேலை வீதங்களை விரைவாகக் கூட்டப் பகுதிகளின் மீ.பொ.ம-வைப் பயன்படுத்தவும்.", "EASY"),
        # Q7
        ("A மற்றும் B ஒரு வேலையை 10 மற்றும் 14 நாட்களில் செய்ய முடியும். இருவரும் 2 நாட்கள் சேர்ந்து வேலை செய்த பின் A விலகுகிறார். மீதமுள்ள வேலைக்கு B-க்குத் தேவையான காலத்தைக் காண்க.",
         ["8.5", "9", "9.2", "10"], 2,
         "ஒருங்கிணைந்த 1 நாள் வேலை = 1/10 + 1/14 = 7/70 + 5/70 = 12/70 = 6/35. 2 நாட்களில் முடிந்த வேலை = 12/35; மீதம் = 23/35. B-இன் வீதம் = 1/14 → காலம் = (23/35) ÷ (1/14) = (23 × 14)/35 = 9.2 நாட்கள். முக்கியக் கற்றல் கருத்து: ஒரே பணியாளருக்கான மீதக் காலத்தைக் கணக்கிடும் முன், ஏற்கெனவே முடிந்த வேலைப் பின்னத்தைக் கண்டறியவும்.", "MEDIUM"),
        # Q8
        ("A, B, C ஒரு வேலையை 6, 9, 18 நாட்களில் முடிக்கின்றனர். மூவரும் சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["2", "3", "4", "5"], 1,
         "மீ.பொ.ம = 18 → A = 3 அலகுகள்/நாள், B = 2 அலகுகள்/நாள், C = 1 அலகு/நாள் → மொத்தம் = 6 அலகுகள்/நாள். காலம் = 18/6 = 3 நாட்கள். முக்கியக் கற்றல் கருத்து: மூன்று அல்லது அதற்கு மேற்பட்ட பணியாளர்கள் இருக்கும்போது, மீ.பொ.ம (அலகு-வேலை) முறை பின்னக் கணக்கீடுகளைத் தவிர்க்கிறது.", "EASY"),
        # Q9
        ("A, B-ஐ விட 25% அதிகத் திறன் உடையவர். B தனியாக 20 நாட்கள் எடுக்கிறார். அவர்களின் ஒருங்கிணைந்த காலத்தைக் காண்க.",
         ["8", "8⁸⁄₉", "9", "10"], 1,
         "திறன் விகிதம் A:B = 5:4 → கால விகிதம் A:B = 4:5. A-இன் காலம் = 20 × 4/5 = 16 நாட்கள். ஒருங்கிணைந்தது = 1/16 + 1/20 = 5/80 + 4/80 = 9/80 → காலம் = 80/9 = 8⁸⁄₉ நாட்கள். முக்கியக் கற்றல் கருத்து: திறன் சதவீதத்தை விகிதமாக மாற்றி, பின்னர் அதைத் தலைகீழாக்கிக் கால விகிதத்தைப் பெறவும்.", "MEDIUM"),
        # Q10
        ("குழாய்கள் A மற்றும் B ஒரு தொட்டியை 8 மற்றும் 12 மணி நேரத்தில் நிரப்புகின்றன; குழாய் C அதை 24 மணி நேரத்தில் காலி செய்கிறது. மூன்றும் ஒரே நேரத்தில் திறக்கப்பட்டால் — நிரம்ப ஆகும் காலத்தைக் காண்க.",
         ["5", "6", "7", "8"], 1,
         "மீ.பொ.ம = 24 → வீதம் = 3/24 + 2/24 − 1/24 = 4/24 = 1/6. காலம் = 6 மணி நேரம். முக்கியக் கற்றல் கருத்து: வெளியேற்றும் குழாயின் வீதம் ஒருங்கிணைந்த நிரப்பும் வீதத்திலிருந்து கழிக்கப்படுகிறது.", "MEDIUM"),
        # Q11
        ("A மற்றும் B ஒரு வேலையை ₹3600-க்கு ஏற்கின்றனர். A தனியாக 9 நாட்களும், B தனியாக 12 நாட்களும் எடுக்கின்றனர். C-இன் உதவியுடன் அவர்கள் 4 நாட்களில் முடிக்கின்றனர். C-இன் பங்கைக் காண்க.",
         ["₹700", "₹750", "₹800", "₹900"], 2,
         "ஒருங்கிணைந்த (A+B) வீதம் = 1/9 + 1/12 = 4/36 + 3/36 = 7/36. C-உடன் தேவையான வீதம் = 1/4 = 9/36. C-இன் வீதம் = 9/36 − 7/36 = 2/36. கூலி விகிதம் A:B:C = 4:3:2 → C-இன் பங்கு = (2/9) × 3600 = ₹800. முக்கியக் கற்றல் கருத்து: அனைவரும் ஒரே எண்ணிக்கையிலான நாட்கள் வேலை செய்யும்போது, கூலி செய்த வேலையின் விகிதத்தில் – அதாவது திறன் விகிதத்தில் – பகிரப்படுகிறது.", "MEDIUM"),
        # Q12
        ("A ஒரு வேலையை 18 நாட்களில் முடிக்க முடியும். A மற்றும் B சேர்ந்து 11 நாட்கள் எடுக்கின்றனர். B தனியாக எடுக்கும் காலத்தைக் காண்க.",
         ["26", "27", "28 2/7", "30"], 2,
         "B-இன் வீதம் = 1/11 − 1/18 = 18/198 − 11/198 = 7/198. B-இன் காலம் = 198/7 = 28 2/7 நாட்கள். முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த வீதத்திலிருந்து A-இன் வீதத்தைக் கழித்து B-இன் வீதத்தைத் தனியாகப் பெறவும்.", "MEDIUM"),
        # Q13
        ("8 ஆண்கள் ஒரு வேலையை 20 நாட்களில் முடிக்கின்றனர். 4 நாட்களுக்குப் பின் மேலும் 4 ஆண்கள் சேர்கின்றனர். வேலையை முடிக்க ஆகும் மொத்த நாட்களைக் காண்க.",
         ["13", "14", "14⅔", "15"], 2,
         "மொத்த வேலை = 8 × 20 = 160 ஆள்-நாட்கள். 4 நாட்களில் முடிந்தது = 32. மீதம் = 128. இப்போது 12 ஆண்கள் → நாட்கள் = 128/12 = 10⅔. மொத்தம் = 4 + 10⅔ = 14⅔ நாட்கள். முக்கியக் கற்றல் கருத்து: மொத்த ஆள்-நாட்களை மாறிலியாகக் கொண்டு, பணியாளர் எண்ணிக்கை மாறிய பின் மீத ஆள்-நாட்களை மீண்டும் கணக்கிடவும்.", "MEDIUM"),
        # Q14
        ("A மற்றும் B ஒரு வேலையை 20 நாட்களிலும்; B மற்றும் C 30 நாட்களிலும்; A மற்றும் C 60 நாட்களிலும் செய்கின்றனர். மூவரும் சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["15", "18", "20", "24"], 2,
         "இணைகளின் கூடுதல் = 1/20 + 1/30 + 1/60. மீ.பொ.ம = 60 → 3/60 + 2/60 + 1/60 = 6/60 = 1/10 = 2(A+B+C). A+B+C = 1/20 → காலம் = 20 நாட்கள். முக்கியக் கற்றல் கருத்து: மூன்று இணை வீதங்களையும் கூட்டினால், மூவரும் சேர்ந்து செய்யும் ஒருங்கிணைந்த வீதத்தின் இருமடங்கு கிடைக்கும்.", "MEDIUM"),
        # Q15
        ("A ஒரு வேலையை 21 நாட்களில் செய்ய முடியும். அவர் 7 நாட்கள் வேலை செய்த பின், மீதமுள்ளதை B 21 நாட்களில் முடிக்கிறார். A மற்றும் B சேர்ந்து எடுக்கும் காலத்தைக் காண்க.",
         ["12", "12.6", "13", "14"], 1,
         "A-இன் 7 நாள் வேலை = 7/21 = 1/3. மீதம் = 2/3; இதை B 21 நாட்களில் செய்கிறார் → B-இன் முழுக் காலம் = 21 ÷ (2/3) = 31.5 நாட்கள். ஒருங்கிணைந்தது = 1/21 + 1/31.5 = 3/63 + 2/63 = 5/63 → காலம் = 63/5 = 12.6 நாட்கள். முக்கியக் கற்றல் கருத்து: ஒவ்வொருவரும் முடித்த வேலைப் பின்னத்திலிருந்து அவரது முழுத் தனிக் காலத்தைக் கண்டறிந்து, பின்னர் வீதங்களை இணைக்கவும்.", "MEDIUM"),
        # Q16
        ("A-இலிருந்து தொடங்கி A மற்றும் B மாற்று நாட்களில் வேலை செய்கின்றனர். A தனியாக 12 நாட்களும், B தனியாக 18 நாட்களும் எடுக்கின்றனர். மொத்தக் காலத்தைக் காண்க.",
         ["13⅔", "14", "14⅓", "15"], 2,
         "மீ.பொ.ம = 36. A = 3 அலகுகள்/நாள், B = 2 அலகுகள்/நாள். 2 நாள் சுழற்சி = 5 அலகுகள். 7 சுழற்சிகள் (14 நாட்கள்) = 35 அலகுகள். மீதம் = 1 அலகு. 15-ஆம் நாள் (A-இன் முறை): A-க்கு 1/3 நாள் தேவை. மொத்தம் = 14 + ⅓ = 14⅓ நாட்கள். முக்கியக் கற்றல் கருத்து: மாற்று நாள் கணக்குகளில், முடிந்தவரை முழுச் சுழற்சிகளை நிறைவு செய்து, பின்னர் இறுதிப் பகுதி நாளைக் கையாளவும்.", "MEDIUM"),
        # Q17
        ("ஒரு நிரப்பும் குழாய் ஒரு தொட்டியை 10 மணி நேரத்தில் நிரப்புகிறது; ஒரு வெளியேற்றும் குழாய் அதை 15 மணி நேரத்தில் காலி செய்கிறது. இரண்டும் ஒரே நேரத்தில் திறக்கப்பட்டால் — நிரம்ப ஆகும் காலத்தைக் காண்க.",
         ["24", "28", "30", "36"], 2,
         "நிகர வீதம் = 1/10 − 1/15 = 3/30 − 2/30 = 1/30. காலம் = 30 மணி நேரம். முக்கியக் கற்றல் கருத்து: நிகர நிரப்பும் வீதம் = நிரப்பும் வீதம் − வெளியேற்றும் வீதம்.", "EASY"),
        # Q18
        ("A ஒரு வேலையை 30 நாட்களில் செய்ய முடியும். B, 25% அதிகத் திறன் உடையவர். ஒருங்கிணைந்த காலத்தைக் காண்க.",
         ["12", "13⅓", "14", "15"], 1,
         "திறன் விகிதம் A:B = 4:5 → B-இன் காலம் = 30 × 4/5 = 24 நாட்கள். ஒருங்கிணைந்தது = 1/30 + 1/24 = 4/120 + 5/120 = 9/120 → காலம் = 120/9 = 13⅓ நாட்கள். முக்கியக் கற்றல் கருத்து: \"x% அதிகத் திறன்\" என்பது ஒரு திறன் விகிதத்தைத் தருகிறது; அதைத் தலைகீழாக்கிக் கால விகிதத்தைப் பெறவும்.", "MEDIUM"),
        # Q19
        ("10 பெண்கள் ஒரு வேலையை 18 நாட்களில் முடிக்கின்றனர்; 6 ஆண்கள் அதை 10 நாட்களில் முடிக்கின்றனர். ஆண் : பெண் திறன் விகிதத்தைக் காண்க.",
         ["2:1", "2.5:1", "3:1", "4:1"], 2,
         "மொத்த வேலை (பெண்கள்) = 10 × 18 = 180 பெண்-நாட்கள். மொத்த வேலை (ஆண்கள்) = 6 × 10 = 60 ஆண்-நாட்கள். 1 ஆண்-நாள் = 180/60 = 3 பெண்-நாட்கள் → திறன் விகிதம் ஆண்:பெண் = 3:1. முக்கியக் கற்றல் கருத்து: இரு குழுக்களின் சார்பு வேலை வீதங்களைக் காண, தேவைப்படும் மொத்த ஆள்-நாட்களை ஒப்பிடவும்.", "EASY"),
        # Q20
        ("A, B, C ஆகியோர் 12, 18, 36 நாட்கள் எடுக்கின்றனர். A 4 நாட்களுக்குப் பின் விலகுகிறார்; B வேலை முடிவதற்கு 3 நாட்களுக்கு முன் விலகுகிறார். மொத்த நாட்களைக் காண்க.",
         ["8", "9", "10", "12"], 2,
         "மீ.பொ.ம = 36. A = 3/நாள், B = 2/நாள், C = 1/நாள். மொத்த நாட்கள் = x என்க. A 4 நாட்கள் வேலை செய்கிறார் = 12 அலகுகள். B (x−3) நாட்கள் வேலை செய்கிறார் = 2(x−3) அலகுகள். C x நாட்கள் வேலை செய்கிறார் = x அலகுகள். 12 + 2(x−3) + x = 36 → 3x + 6 = 36 → x = 10 நாட்கள். முக்கியக் கற்றல் கருத்து: ஒவ்வொரு பணியாளரின் பங்களிப்பையும் தெரியாத மொத்த நாட்களின் அடிப்படையில் வெளிப்படுத்தி இயற்கணித முறையில் தீர்க்கவும்.", "MEDIUM"),
        # Q21
        ("A ஒரு சுவரை 10 நாட்களிலும், B 15 நாட்களிலும் கட்டுகின்றனர்; C அதை 15 நாட்களில் இடிக்கிறார். அனைவரும் சேர்ந்து வேலை செய்தால் — சுவர் முடிய ஆகும் காலத்தைக் காண்க.",
         ["8", "9", "10", "12"], 2,
         "மீ.பொ.ம = 30. A = 3, B = 2, C = −2 (இடித்தல்) → நிகரம் = 3 அலகுகள்/நாள். காலம் = 30/3 = 10 நாட்கள். முக்கியக் கற்றல் கருத்து: இடிப்பவர் ஒருங்கிணைந்த வேலைச் சமன்பாட்டில் எதிர்மறை வீதமாகச் செயல்படுகிறார்.", "MEDIUM"),
        # Q22
        ("ஓர் ஒப்பந்ததாரர் 25 நாள் திட்டத்திற்கு 30 பணியாளர்களை அமர்த்துகிறார். 10 நாட்களுக்குப் பின், 1/3 பகுதி மட்டுமே முடிந்துள்ளது. மேலும் எத்தனை பணியாளர்கள் தேவை?",
         ["5", "8", "10", "12"], 2,
         "30 பணியாளர்கள் × 10 நாட்கள் = 300 ஆள்-நாட்களில் வேலையின் 1/3 பகுதி முடிந்தது → மொத்த வேலை = 900 ஆள்-நாட்கள். மீத வேலை = 600 ஆள்-நாட்கள்; இதை மீதமுள்ள 15 நாட்களில் முடிக்க வேண்டும் → தேவையான பணியாளர்கள் = 600/15 = 40. கூடுதல் பணியாளர்கள் = 40 − 30 = 10. முக்கியக் கற்றல் கருத்து: மொத்த வேலையைத் திட்டமிட்ட வேகத்தின் அடிப்படையில் அல்லாமல், உண்மையில் காணப்பட்ட வேகத்தின் அடிப்படையில் மீண்டும் கணக்கிடவும்.", "MEDIUM"),
        # Q23
        ("A மற்றும் B-க்கு மொத்தம் ₹7200 வழங்கப்படுகிறது. A தனியாக 6 நாட்களும், B தனியாக 9 நாட்களும் எடுக்கின்றனர். B-இன் பங்கைக் காண்க.",
         ["2400", "2600", "2880", "3000"], 2,
         "திறன் விகிதம் A:B = (1/6):(1/9) = 3:2. B-இன் பங்கு = (2/5) × 7200 = ₹2,880. முக்கியக் கற்றல் கருத்து: கூலிப் பங்கு கால விகிதத்தை நேரடியாக அல்லாமல், திறன் விகிதத்தை (1/காலம்) பின்பற்றுகிறது.", "MEDIUM"),
        # Q24
        ("A ஒரு வேலையின் 2/5 பகுதியை 8 நாட்களில் செய்கிறார்; B அவ்வேலையின் 1/3 பகுதியை 10 நாட்களில் செய்கிறார். இருவரும் சேர்ந்து வேலை செய்தால் எடுக்கும் காலத்தைக் காண்க.",
         ["10", "11", "12", "15"], 2,
         "A-இன் முழுக் காலம் = 8 ÷ (2/5) = 20 நாட்கள் → வீதம் = 1/20. B-இன் முழுக் காலம் = 10 ÷ (1/3) = 30 நாட்கள் → வீதம் = 1/30. ஒருங்கிணைந்தது = 1/20 + 1/30 = 3/60 + 2/60 = 5/60 = 1/12 → காலம் = 12 நாட்கள். முக்கியக் கற்றல் கருத்து: முழுக் காலம் = (எடுத்த நாட்கள்) ÷ (முடித்த வேலைப் பின்னம்). வீதங்களை இணைக்கும் முன் ஒவ்வொரு பகுதி-வேலைக் கூற்றையும் மாற்றவும்.", "MEDIUM"),
        # Q25
        ("5 ஆண்களும் 4 பெண்களும் ஒரு வேலையை 9 நாட்களில் முடிக்கின்றனர்; 3 ஆண்களும் 6 பெண்களும் அதை 10 நாட்களில் முடிக்கின்றனர். ஆண் : பெண் வேலை வீத விகிதத்தைக் காண்க.",
         ["5:3", "7:4", "8:5", "9:5"], 2,
         "ஆணின் வீதம் = m, பெண்ணின் வீதம் = w என்க. 5m + 4w = 1/9 மற்றும் 3m + 6w = 1/10. மொத்த வேலை ஒன்றே: 9(5m + 4w) = 10(3m + 6w) ⟹ 45m + 36w = 30m + 60w ⟹ 15m = 24w. m : w = 24 : 15 = 8 : 5. முக்கியக் கற்றல் கருத்து: தனி வீதங்களைத் தொடர்புபடுத்த, இரண்டு சூழல்களிலும் உள்ள மொத்த வேலையை (குழு வீதம் × நாட்கள்) சமப்படுத்தவும்.", "HARD"),
        # Q26
        ("A ‘x’ நாட்களும், B ‘x+8’ நாட்களும் எடுக்கின்றனர்; இருவரும் சேர்ந்து 7½ நாட்கள் எடுக்கின்றனர். x-ஐக் காண்க.",
         ["10", "11", "12", "14"], 2,
         "1/x + 1/(x+8) = 2/15. 15(2x + 8) = 2x(x + 8) ⟹ 30x + 120 = 2x² + 16x ⟹ x² − 7x − 60 = 0. (x − 12)(x + 5) = 0 → x = 12 (எதிர்மறை மூலத்தை நீக்கி). சரிபார்ப்பு: 1/12 + 1/20 = 5/60 + 3/60 = 8/60 = 2/15 ✓. முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த வேலைச் சமன்பாட்டிலிருந்து ஓர் இருபடிச் சமன்பாட்டை அமைத்து, எதிர்மறை மூலத்தை நீக்கி, விடையைச் சரிபார்க்கவும்.", "MEDIUM"),
        # Q27
        ("A நாளொன்றுக்கு 10 மணி நேரம் வேலை செய்து ஒரு வேலையை 12 நாட்களில் முடிக்கிறார். நாளொன்றுக்கு 8 மணி நேரம் என்றால் எத்தனை நாட்கள் ஆகும்?",
         ["12", "14", "15", "18"], 2,
         "மொத்த வேலை = 12 × 10 = 120 மணி நேரம். நாளொன்றுக்கு 8 மணி நேரம் → 120/8 = 15 நாட்கள். முக்கியக் கற்றல் கருத்து: மொத்த வேலை மணி நேரமாக மாற்றி, பின்னர் புதிய தினசரி மணி நேரத்தால் வகுக்கவும்.", "EASY"),
        # Q28
        ("இரண்டு குழாய்கள் ஒரு நீர்த்தொட்டியை 10 மற்றும் 15 நிமிடங்களில் நிரப்புகின்றன; ஒரு வடிகால் அதை 6 நிமிடங்களில் காலி செய்கிறது. மூன்றும் ஒரே நேரத்தில் திறக்கப்பட்டால் — தொட்டி நிரம்புமா/காலியாகுமா, எவ்வளவு நேரத்தில் எனக் காண்க.",
         ["நிரம்பும், 30 நிமி", "காலியாகும், 30 நிமி", "மாறாமல் இருக்கும் (நிகர வீதம் பூஜ்ஜியம்)", "நிரம்பும், 36 நிமி"], 2,
         "நிகர வீதம் = 1/10 + 1/15 − 1/6. மீ.பொ.ம = 30 → 3/30 + 2/30 − 5/30 = 0. நிகர வீதம் பூஜ்ஜியம்; எனவே நீர்மட்டம் மாறாமல் இருக்கும். முக்கியக் கற்றல் கருத்து: முதலில் நிகர வீதத்தின் குறியைச் சரிபார்க்கவும்: நேர்மறை என்றால் நிரம்பும், எதிர்மறை என்றால் காலியாகும், பூஜ்ஜியம் என்றால் மாற்றமில்லை.", "MEDIUM"),
        # Q29
        ("A, B, C சேர்ந்து ஒரு வேலையை 4 நாட்களில் முடிக்கின்றனர். A தனியாக 9 நாட்களும், B தனியாக 12 நாட்களும் எடுக்கின்றனர். C தனியாக எடுக்கும் காலத்தைக் காண்க.",
         ["15", "16", "18", "20"], 2,
         "A+B = 1/9 + 1/12 = 4/36 + 3/36 = 7/36. C-இன் வீதம் = 1/4 − 7/36 = 9/36 − 7/36 = 2/36 = 1/18. C தனியாக = 18 நாட்கள். முக்கியக் கற்றல் கருத்து: தெரியாத பணியாளரின் வீதத்தைத் தனியாகப் பெற, ஒருங்கிணைந்த வீதத்திலிருந்து தெரிந்த பணியாளர்களின் வீதங்களின் கூடுதலைக் கழிக்கவும்.", "MEDIUM"),
        # Q30
        ("20 பணியாளர்கள் ஒரு பணியை 18 நாட்களில் முடிக்கின்றனர். 6 நாட்களுக்குப் பின் 4 பணியாளர்கள் விலகுகின்றனர். பணியை முடிக்க ஆகும் மொத்த நாட்களைக் காண்க.",
         ["18", "20", "21", "24"], 2,
         "மொத்த வேலை = 20 × 18 = 360 பணியாளர்-நாட்கள். 6 நாட்களில் முடிந்தது = 120. மீதம் = 240. இப்போது 16 பணியாளர்கள் → 240/16 = 15 நாட்கள். மொத்தம் = 6 + 15 = 21 நாட்கள். முக்கியக் கற்றல் கருத்து: பணியாளர் எண்ணிக்கை குறைந்த பின் மீதமுள்ள பணியாளர்-நாட்களை மீண்டும் கணக்கிடவும்.", "MEDIUM")
    ]

    out_lines = [
        "/* ============================================================================",
        "   ExamPro LMS - Time and Work Course Seed Script (Unified Bilingual Model)",
        "   - 1 Course: Time and Work / காலம் மற்றும் வேலை",
        "   - 2 Assessments (Single unified assessment for both English & Tamil):",
        "       1. Time and Work - Practice Set (time-and-work-practice) [55 Questions]",
        "          (25 Worked Examples + 30 Independent Practice in both English & Tamil)",
        "       2. Time and Work - Graded Assessment (time-and-work-graded) [30 Questions]",
        "          (Assessment Questions 1-30 in both English & Tamil)",
        "   ============================================================================ */",
        "USE ExamProLMS;",
        "GO",
        "SET QUOTED_IDENTIFIER ON;",
        "GO",
        "",
        "-- Step 1: Ensure bilingual columns exist in dbo.Assessments & dbo.Questions",
        "IF COL_LENGTH(N'dbo.Assessments', N'TitleTa') IS NULL",
        "    ALTER TABLE dbo.Assessments ADD TitleTa NVARCHAR(200) NULL;",
        "IF COL_LENGTH(N'dbo.Assessments', N'DescriptionTa') IS NULL",
        "    ALTER TABLE dbo.Assessments ADD DescriptionTa NVARCHAR(MAX) NULL;",
        "IF COL_LENGTH(N'dbo.Questions', N'QuestionTextTa') IS NULL",
        "    ALTER TABLE dbo.Questions ADD QuestionTextTa NVARCHAR(MAX) NULL;",
        "IF COL_LENGTH(N'dbo.Questions', N'OptionsJsonTa') IS NULL",
        "    ALTER TABLE dbo.Questions ADD OptionsJsonTa NVARCHAR(MAX) NULL;",
        "IF COL_LENGTH(N'dbo.Questions', N'ExplanationTa') IS NULL",
        "    ALTER TABLE dbo.Questions ADD ExplanationTa NVARCHAR(MAX) NULL;",
        "GO",
        "",
        "BEGIN TRANSACTION;",
        "",
        "-- Clean previous Time and Work courses and assessments if present",
        "DELETE FROM dbo.Assessments WHERE Slug IN (",
        "    N'time-and-work-practice', N'time-and-work-graded',",
        "    N'time-work-practice', N'time-work-graded',",
        "    N'time-and-work-practice-en', N'time-and-work-graded-en',",
        "    N'time-and-work-practice-ta', N'time-and-work-graded-ta'",
        ");",
        "DELETE FROM dbo.Courses WHERE Slug IN (N'time-and-work', N'time-work');",
        "",
        "INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)",
        "VALUES (",
        "    N'Time and Work / காலம் மற்றும் வேலை',",
        "    N'time-and-work',",
        "    N'Comprehensive arithmetic and reasoning module on Time and Work, Pipes & Cisterns, and Wages for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',",
        "    3",
        ");",
        "",
        "DECLARE @CourseId INT = SCOPE_IDENTITY();",
        "",
        "-- Insert ONLY 2 Assessments: 1 Practice (55 Questions) and 1 Graded (30 Questions)",
        "INSERT INTO dbo.Assessments (",
        "    CourseId, Title, TitleTa, Slug, Description, DescriptionTa, Topic, Difficulty,",
        "    DefaultDurationMinutes, MinDurationMinutes, TotalQuestions, PassPercentage,",
        "    AttemptType, SequentialUnlock, LockdownEnabled, ProctoringEnabled, OrderIndex",
        ")",
        "VALUES",
        "    (@CourseId, N'Time and Work - Practice Set', N'காலம் மற்றும் வேலை - பயிற்சித் தொகுப்பு', N'time-and-work-practice',",
        "     N'55 practice questions (Worked Examples + Independent Practice) with instant feedback & step-by-step solutions.',",
        "     N'55 பயிற்சிக் கணக்குகள் (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனடித் தீர்வுகளுடன்.',",
        "     N'Time and Work', N'EASY', 60, 10, 55, 0, N'PRACTICE', 0, 0, 0, 1),",
        "    (@CourseId, N'Time and Work - Graded Assessment', N'காலம் மற்றும் வேலை - மதிப்பீட்டுத் தேர்வு', N'time-and-work-graded',",
        "     N'Official proctored & timed assessment on Time and Work (30 Questions). Pass with 60% to master this topic.',",
        "     N'காலம் மற்றும் வேலைக்கான அதிகாரப்பூர்வக் கண்காணிப்புடன் கூடிய தேர்வு (30 வினாக்கள்). தேர்ச்சி 60%.',",
        "     N'Time and Work', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 2);",
        "",
        "DECLARE @pracId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'time-and-work-practice');",
        "DECLARE @gradId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'time-and-work-graded');",
        ""
    ]

    def insert_bilingual_questions(target_var: str, en_items: list, ta_items: list):
        out_lines.append(f"-- Insert bilingual questions for {target_var} ({len(en_items)} questions)")
        out_lines.append("INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, QuestionTextTa, OptionsJsonTa, ExplanationTa, Topic, Difficulty, OrderIndex)")
        out_lines.append("VALUES")
        val_rows = []
        for idx in range(len(en_items)):
            en_q, en_opts, ans_idx, en_expl, diff = en_items[idx]
            ta_q, ta_opts, _, ta_expl, _ = ta_items[idx]
            en_opts_json = json.dumps(en_opts, ensure_ascii=False)
            ta_opts_json = json.dumps(ta_opts, ensure_ascii=False)

            row = (
                f"    ({target_var}, "
                f"{escape_sql(en_q)}, {escape_sql(en_opts_json)}, {ans_idx}, {escape_sql(en_expl)}, "
                f"{escape_sql(ta_q)}, {escape_sql(ta_opts_json)}, {escape_sql(ta_expl)}, "
                f"N'Time and Work', {escape_sql(diff)}, {idx + 1})"
            )
            val_rows.append(row)
        out_lines.append(",\n".join(val_rows) + ";\n")

    # 1. Practice Set (55 Questions: 25 worked + 30 indep)
    insert_bilingual_questions("@pracId", worked_en + indep_en, worked_ta + indep_ta)

    # 2. Graded Assessment (30 Questions)
    insert_bilingual_questions("@gradId", graded_en, graded_ta)

    out_lines.append("COMMIT;")
    out_lines.append("PRINT 'Time and Work Course seeded successfully: 1 Practice Assessment (55 Qs) and 1 Graded Assessment (30 Qs), fully bilingual (English & Tamil).';")
    out_lines.append("GO\n")

    output_path = r"c:\Users\Lenovo\Downloads\LMS\exampro-lms\database\06_time_and_work_bilingual_seed.sql"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Successfully generated {output_path} with {len(worked_en) + len(indep_en)} practice and {len(graded_en)} graded questions.")

if __name__ == "__main__":
    main()
