# -*- coding: utf-8 -*-
"""Generates 05_ratio_bilingual_seed.sql containing all 85 questions from English and Tamil Ratio and Proportion PDFs."""
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
        ("On a map with a scale of 1:1,00,000, the area of a forest reserve is shown as 8 sq. cm. Find the actual area of the reserve in sq. km. (1 km = 1,00,000 cm)",
         ["6 sq. km", "7 sq. km", "8 sq. km", "9 sq. km"], 2,
         "Area scale = (1,00,000)². Actual area = 8 × (1,00,000)² cm² = 8 × 10¹⁰ cm². Converting to km² (÷ 10¹⁰): Actual area = 8 sq. km. Key Learning Point: Map-to-actual area conversions always apply the duplicate (squared) ratio of the linear map scale.", "EASY"),
        # Q2
        ("In a survey of 800 people, the number who like tea only, coffee only, both, and neither are in the ratio 4:3:2:1. Find the number of people who like at least one of the two beverages.",
         ["650", "680", "700", "720"], 3,
         "Total parts = 4 + 3 + 2 + 1 = 10; value of 1 part = 800/10 = 80. People who like at least one = tea only + coffee only + both = (4 + 3 + 2) parts = 9 parts = 9 × 80 = 720. Key Learning Point: 'At least one' excludes only the 'neither' category, so add all parts except the neither-part before multiplying.", "MEDIUM"),
        # Q3
        ("A sum of money is divided among A, B and C in the ratio 4:5:6. If C receives ₹300 more than A, find A's share.",
         ["₹500", "₹550", "₹600", "₹650"], 2,
         "Difference between C's and A's parts = 6 − 4 = 2 parts = ₹300. 1 part = ₹150. A's share = 4 parts = 150 × 4 = ₹600. Key Learning Point: Once the value of one part is known from the difference, any individual share can be found directly.", "EASY"),
        # Q4
        ("Find the fourth proportional to 6, 8, and 15.",
         ["18", "20", "22", "24"], 1,
         "6 : 8 :: 15 : x. 6x = 8 × 15 ⟹ x = 120/6 = 20. Key Learning Point: For the fourth proportional to a, b, c: x = (b × c)/a.", "EASY"),
        # Q5
        ("Find the mean proportion between 4 and 16.",
         ["6", "8", "10", "12"], 1,
         "Mean proportion = √(4 × 16) = √64 = 8. Key Learning Point: The mean proportion between a and b is √(a × b).", "EASY"),
        # Q6
        ("The ratio of the populations of two towns is 5:4. The population of the first town increases by 20% and the second by 25%. Find the new ratio of their populations.",
         ["6:5", "7:5", "9:5", "9:8"], 0,
         "New population of town 1 = 5 × (6/5) = 6. New population of town 2 = 4 × (5/4) = 5. New ratio = 6 : 5. Key Learning Point: Track each quantity's own percentage change separately — do not apply a combined or average percentage to the whole ratio.", "MEDIUM"),
        # Q7
        ("6 men or 9 women can complete a piece of work in the same number of days. Find the ratio of the efficiency of one man to one woman.",
         ["2:3", "3:2", "4:3", "3:4"], 1,
         "6 × (man's efficiency) = 9 × (woman's efficiency). Man's efficiency : Woman's efficiency = 9 : 6 = 3 : 2. Key Learning Point: Set the total work done by each group equal, since they complete the same work in the same time.", "EASY"),
        # Q8
        ("The cost of 15 articles is ₹450. Find the cost of 40 articles at the same rate.",
         ["₹1,000", "₹1,100", "₹1,200", "₹1,300"], 2,
         "Cost varies directly with the number of articles. 15 : 450 :: 40 : x. x = (450 × 40)/15 = ₹1,200. Key Learning Point: When quantities vary directly, set up a proportion and cross-multiply.", "EASY"),
        # Q9
        ("A invests ₹6,000 for 9 months and B invests ₹8,000 for 6 months in a business. If the total profit is ₹7,650, find B's share.",
         ["₹3,200", "₹3,400", "₹3,600", "₹3,800"], 2,
         "Ratio of investment-months: A = 6000 × 9 = 54,000; B = 8000 × 6 = 48,000. Ratio = 54,000 : 48,000 = 9 : 8. B's share = (8/17) × 7650 = ₹3,600. Key Learning Point: The profit-sharing ratio is based on capital-time product, so unequal durations must be accounted for.", "MEDIUM"),
        # Q10
        ("The speeds of two trains are in the ratio 4:5. If the slower train covers 180 km in 4.5 hours, find the speed of the faster train.",
         ["45 km/h", "50 km/h", "55 km/h", "60 km/h"], 1,
         "Speed of slower train = 180/4.5 = 40 km/h. Speed ratio: faster/slower = 5/4. Speed of faster train = (5/4) × 40 = 50 km/h. Key Learning Point: Divide distance by time to get the known speed, then apply the ratio to find the other speed.", "EASY"),
        # Q11
        ("A can complete a piece of work in 20 days and B can complete the same work in 30 days. If they work together, in how many days will the work be completed?",
         ["10 days", "11 days", "12 days", "13 days"], 2,
         "A's 1-day work = 1/20; B's 1-day work = 1/30. Combined 1-day work = 1/20 + 1/30 = 3/60 + 2/60 = 5/60 = 1/12. Time taken together = 12 days. Key Learning Point: The combined rate of two workers is the sum of their individual rates, not the average of their individual times.", "EASY"),
        # Q12
        ("Two numbers are in the ratio 7:9. If each number is increased by 6, the ratio becomes 9:11. Find the numbers.",
         ["14 and 18", "21 and 27", "28 and 36", "35 and 45"], 1,
         "Let the numbers be 7x and 9x. (7x + 6)/(9x + 6) = 9/11. 11(7x + 6) = 9(9x + 6) ⟹ 77x + 66 = 81x + 54 ⟹ 4x = 12 ⟹ x = 3. Numbers = 7(3) = 21 and 9(3) = 27. Key Learning Point: When a fixed value is added to both terms of a ratio, form an equation using the new ratio and solve for the multiplier.", "MEDIUM"),
        # Q13
        ("The sum of two numbers is 350. If 20 is added to each number, the ratio of the new numbers becomes 6:7. Find the two numbers.",
         ["150 and 180", "155 and 185", "160 and 190", "165 and 195"], 2,
         "a + b = 350. After adding 20 to each: (a+20) + (b+20) = 390. Splitting 390 in the ratio 6:7 gives a+20 = 180, b+20 = 210. So a = 160 and b = 190. Key Learning Point: This problem combines two ratio skills: adjusting the total sum for the added constant, then dividing in the new ratio.", "MEDIUM"),
        # Q14
        ("Two numbers are in the ratio 7:9. If the sum of their squares is 1,170, find the larger number.",
         ["21", "24", "27", "30"], 2,
         "Let the numbers be 7k and 9k. 49k² + 81k² = 1170 ⟹ 130k² = 1170 ⟹ k² = 9 ⟹ k = 3. Larger number = 9k = 9 × 3 = 27. Key Learning Point: Set up the sum-of-squares equation using the ratio multiples, then solve for k before finding the required number.", "MEDIUM"),
        # Q15
        ("If 10 workers working 6 hours a day earn ₹7,200 in total, how much will 15 workers working 8 hours a day earn, at the same rate?",
         ["₹13,200", "₹13,800", "₹14,400", "₹15,000"], 2,
         "Rate per worker-hour = 7200 / (10 × 6) = ₹120. New earnings = 120 × (15 × 8) = ₹14,400. Key Learning Point: When a quantity depends on two variables at once, compute a single combined rate before applying it to the new values.", "MEDIUM"),
        # Q16
        ("Divide ₹1,200 between two people in the ratio 5:7.",
         ["₹450 and ₹750", "₹500 and ₹700", "₹520 and ₹680", "₹480 and ₹720"], 1,
         "Total parts = 5 + 7 = 12. First share = (5/12) × 1200 = ₹500. Second share = (7/12) × 1200 = ₹700. Key Learning Point: Divide the total by the sum of the ratio parts before multiplying by each part.", "EASY"),
        # Q17
        ("The present ages of two brothers are in the ratio 5:7. After 6 years, the ratio of their ages will be 4:5. Find their present ages.",
         ["8 and 12 years", "10 and 14 years", "12 and 16 years", "14 and 18 years"], 1,
         "Let present ages be 5x and 7x. (5x + 6)/(7x + 6) = 4/5. 5(5x + 6) = 4(7x + 6) ⟹ 25x + 30 = 28x + 24 ⟹ x = 2. Present ages = 5(2) = 10 years and 7(2) = 14 years. Key Learning Point: Translate the 'after n years' condition into an equation with the new ratio before solving for x.", "MEDIUM"),
        # Q18
        ("A bag contains ₹1, 50 paise, and 25 paise coins in the ratio 3:4:5. If the total value of the coins is ₹500, find the number of 25 paise coins.",
         ["350", "380", "400", "420"], 2,
         "Let the coins be 3x, 4x, 5x. Value = 3x(1) + 4x(0.5) + 5x(0.25) = 3x + 2x + 1.25x = 6.25x. 6.25x = 500 ⟹ x = 80. Number of 25 paise coins = 5x = 400. Key Learning Point: Convert every coin type's count to its rupee value before adding, since the ratio of coins differs from the ratio of value.", "MEDIUM"),
        # Q19
        ("A container has 27 litres of pure milk. One-third of the mixture is withdrawn and replaced with water. Find the quantity of milk left in the container.",
         ["16 litres", "17 litres", "18 litres", "19 litres"], 2,
         "Fraction removed = 1/3; fraction remaining = 2/3. Milk left = 27 × (2/3) = 18 litres. Key Learning Point: A single replacement operation simply scales the milk quantity by the fraction remaining.", "EASY"),
        # Q20
        ("A bag contains ₹1, 50 paise, and 25 paise coins in the ratio 5:6:8. If the total value of the coins is ₹210, find the number of 25 paise coins.",
         ["144", "156", "168", "180"], 2,
         "Let the number of coins be 5x, 6x and 8x. Value = 5x(1) + 6x(0.5) + 8x(0.25) = 5x + 3x + 2x = 10x. 10x = 210 ⟹ x = 21. Number of 25 paise coins = 8x = 168. Key Learning Point: When ratios involve coins of different denominations, convert the count of each type to its value before summing.", "MEDIUM"),
        # Q21
        ("Two numbers are in the ratio 5:6. If 8 is subtracted from each, the ratio becomes 4:5. Find the numbers.",
         ["30 and 36", "35 and 42", "40 and 48", "45 and 54"], 2,
         "Let the numbers be 5x and 6x. (5x − 8)/(6x − 8) = 4/5. 5(5x − 8) = 4(6x − 8) ⟹ 25x − 40 = 24x − 32 ⟹ x = 8. Numbers = 5(8) = 40 and 6(8) = 48. Key Learning Point: When a fixed value is subtracted from both terms, set up an equation with the new ratio and solve for x.", "MEDIUM"),
        # Q22
        ("Simplify the ratio 84:126.",
         ["1:2", "2:3", "3:4", "4:5"], 1,
         "Ratio = 84 : 126. HCF of 84 and 126 = 42. 84 ÷ 42 : 126 ÷ 42 = 2 : 3. Key Learning Point: Always divide both terms of a ratio by their HCF to express it in simplest form.", "EASY"),
        # Q23
        ("Three numbers are in continued proportion. If the first number is 16 and the third is 25, find the sum of all three numbers.",
         ["59", "60", "61", "62"], 2,
         "b² = a × c = 16 × 25 = 400 ⟹ b = 20. Sum = 16 + 20 + 25 = 61. Key Learning Point: Always verify that the mean proportional found is a whole number before proceeding, since competitive exam values are usually chosen for clean results.", "MEDIUM"),
        # Q24
        ("A mixture of 32 litres contains milk and water in the ratio 3:1. How much water must be added to make the ratio of milk to water 3:2?",
         ["6 litres", "7 litres", "8 litres", "9 litres"], 2,
         "Milk = (3/4) × 32 = 24 litres; Water = (1/4) × 32 = 8 litres. For milk : water = 3 : 2, water required = 24 × (2/3) = 16 litres. Water to be added = 16 − 8 = 8 litres. Key Learning Point: Find the fixed quantity (milk) first, then use the target ratio to find the required water.", "MEDIUM"),
        # Q25
        ("A, B and C start a business with capitals of ₹2,000, ₹3,000 and ₹4,000. A and B invest for 12 months, and C invests for 9 months. If the total profit is ₹7,000, find A's share.",
         ["₹1,500", "₹1,750", "₹2,000", "₹2,250"], 1,
         "Capital-time: A = 2000 × 12 = 24,000; B = 3000 × 12 = 36,000; C = 4000 × 9 = 36,000. Ratio = 24,000 : 36,000 : 36,000 = 2 : 3 : 3. Total parts = 8; A's share = (2/8) × 7000 = ₹1,750. Key Learning Point: Compute each partner's capital-time product individually before forming the combined ratio.", "MEDIUM")
    ]

    # 25 Worked Examples (Tamil)
    worked_ta = [
        # Q1
        ("1:1,00,000 அளவுகோல் கொண்ட ஒரு வரைபடத்தில், ஒரு காப்புக் காட்டின் பரப்பு 8 ச.செ.மீ ஆகக் காட்டப்பட்டுள்ளது. அக்காப்புக் காட்டின் உண்மையான பரப்பை ச.கி.மீ-இல் காண்க. (1 கி.மீ = 1,00,000 செ.மீ)",
         ["6 ச.கி.மீ", "7 ச.கி.மீ", "8 ச.கி.மீ", "9 ச.கி.மீ"], 2,
         "பரப்பு அளவுகோல் = (1,00,000)². உண்மையான பரப்பு = 8 × (1,00,000)² செ.மீ² = 8 × 10¹⁰ செ.மீ². கி.மீ²-ஆக மாற்ற (÷ 10¹⁰): உண்மையான பரப்பு = 8 ச.கி.மீ. முக்கியக் கற்றல் கருத்து: வரைபடப் பரப்பை உண்மையான பரப்பாக மாற்றும்போது, நேரியல் வரைபட அளவுகோலின் இருமடி (வர்க்க) விகிதமே எப்போதும் பயன்படுத்தப்படுகிறது.", "EASY"),
        # Q2
        ("800 பேரிடம் நடத்தப்பட்ட ஒரு கணக்கெடுப்பில், தேநீர் மட்டும், காபி மட்டும், இரண்டும், எதுவுமில்லை என விரும்புவோரின் எண்ணிக்கை 4:3:2:1 என்ற விகிதத்தில் உள்ளது. இரண்டு பானங்களில் குறைந்தது ஒன்றை விரும்புவோரின் எண்ணிக்கையைக் காண்க.",
         ["650", "680", "700", "720"], 3,
         "மொத்தப் பகுதிகள் = 4 + 3 + 2 + 1 = 10; 1 பகுதியின் மதிப்பு = 800/10 = 80. குறைந்தது ஒன்றை விரும்புவோர் = தேநீர் மட்டும் + காபி மட்டும் + இரண்டும் = (4 + 3 + 2) பகுதிகள் = 9 பகுதிகள் = 9 × 80 = 720. முக்கியக் கற்றல் கருத்து: 'குறைந்தது ஒன்று' என்பது 'எதுவுமில்லை' என்ற வகையை மட்டுமே விலக்குகிறது; எனவே பெருக்கும் முன் 'எதுவுமில்லை' பகுதியைத் தவிர மற்ற அனைத்துப் பகுதிகளையும் கூட்டவும்.", "MEDIUM"),
        # Q3
        ("ஒரு தொகை A, B, C ஆகியோருக்கு 4:5:6 என்ற விகிதத்தில் பிரிக்கப்படுகிறது. A-ஐ விட C ₹300 அதிகம் பெற்றால், A-இன் பங்கைக் காண்க.",
         ["₹500", "₹550", "₹600", "₹650"], 2,
         "C மற்றும் A-இன் பகுதிகளுக்கிடையிலான வேறுபாடு = 6 − 4 = 2 பகுதிகள் = ₹300. 1 பகுதி = ₹150. A-இன் பங்கு = 4 பகுதிகள் = 150 × 4 = ₹600. முக்கியக் கற்றல் கருத்து: வேறுபாட்டிலிருந்து ஒரு பகுதியின் மதிப்பு தெரிந்தவுடன், எந்தத் தனிப்பங்கையும் நேரடியாகக் காணலாம்.", "EASY"),
        # Q4
        ("6, 8, 15 ஆகியவற்றின் நான்காம் விகிதசம உறுப்பைக் காண்க.",
         ["18", "20", "22", "24"], 1,
         "6 : 8 :: 15 : x. 6x = 8 × 15 ⟹ x = 120/6 = 20. முக்கியக் கற்றல் கருத்து: a, b, c-இன் நான்காம் விகிதசம உறுப்பு: x = (b × c)/a.", "EASY"),
        # Q5
        ("4 மற்றும் 16-இன் இடை விகிதசம உறுப்பைக் காண்க.",
         ["6", "8", "10", "12"], 1,
         "இடை விகிதசம உறுப்பு = √(4 × 16) = √64 = 8. முக்கியக் கற்றல் கருத்து: a மற்றும் b-இன் இடை விகிதசம உறுப்பு √(a × b) ஆகும்.", "EASY"),
        # Q6
        ("இரண்டு நகரங்களின் மக்கள்தொகை விகிதம் 5:4. முதல் நகரத்தின் மக்கள்தொகை 20%, இரண்டாவது நகரத்தின் மக்கள்தொகை 25% அதிகரிக்கிறது. அவற்றின் மக்கள்தொகையின் புதிய விகிதத்தைக் காண்க.",
         ["6:5", "7:5", "9:5", "9:8"], 0,
         "நகரம் 1-இன் புதிய மக்கள்தொகை = 5 × (6/5) = 6. நகரம் 2-இன் புதிய மக்கள்தொகை = 4 × (5/4) = 5. புதிய விகிதம் = 6 : 5. முக்கியக் கற்றல் கருத்து: ஒவ்வோர் அளவின் சொந்தச் சதவீத மாற்றத்தையும் தனித்தனியாகக் கணக்கிடவும் — முழு விகிதத்திற்கும் ஒருங்கிணைந்த அல்லது சராசரிச் சதவீதத்தைப் பயன்படுத்தக் கூடாது.", "MEDIUM"),
        # Q7
        ("6 ஆண்கள் அல்லது 9 பெண்கள் ஒரு வேலையை ஒரே எண்ணிக்கையிலான நாட்களில் முடிக்க முடியும். ஓர் ஆணுக்கும் ஒரு பெண்ணுக்கும் இடையிலான திறன் விகிதத்தைக் காண்க.",
         ["2:3", "3:2", "4:3", "3:4"], 1,
         "6 × (ஆணின் திறன்) = 9 × (பெண்ணின் திறன்). ஆணின் திறன் : பெண்ணின் திறன் = 9 : 6 = 3 : 2. முக்கியக் கற்றல் கருத்து: இரண்டு குழுக்களும் ஒரே வேலையை ஒரே காலத்தில் முடிப்பதால், ஒவ்வொரு குழுவும் செய்யும் மொத்த வேலையைச் சமப்படுத்தவும்.", "EASY"),
        # Q8
        ("15 பொருட்களின் விலை ₹450. அதே விலையில் 40 பொருட்களின் விலையைக் காண்க.",
         ["₹1,000", "₹1,100", "₹1,200", "₹1,300"], 2,
         "விலை பொருட்களின் எண்ணிக்கைக்கு நேர் விகிதத்தில் மாறுகிறது. 15 : 450 :: 40 : x. x = (450 × 40)/15 = ₹1,200. முக்கியக் கற்றல் கருத்து: அளவுகள் நேர் விகிதத்தில் மாறும்போது, விகிதசமத்தை அமைத்துக் குறுக்குப் பெருக்கல் செய்யவும்.", "EASY"),
        # Q9
        ("ஒரு வியாபாரத்தில் A ₹6,000-ஐ 9 மாதங்களுக்கும், B ₹8,000-ஐ 6 மாதங்களுக்கும் முதலீடு செய்கின்றனர். மொத்த இலாபம் ₹7,650 எனில், B-இன் பங்கைக் காண்க.",
         ["₹3,200", "₹3,400", "₹3,600", "₹3,800"], 2,
         "முதலீடு-மாதங்களின் விகிதம்: A = 6000 × 9 = 54,000; B = 8000 × 6 = 48,000. விகிதம் = 54,000 : 48,000 = 9 : 8. B-இன் பங்கு = (8/17) × 7650 = ₹3,600. முக்கியக் கற்றல் கருத்து: இலாபப் பகிர்வு விகிதம் முதலீடு × காலம் என்ற பெருக்கற்பலனை அடிப்படையாகக் கொண்டது; எனவே சமமற்ற காலங்களைக் கணக்கில் கொள்ள வேண்டும்.", "MEDIUM"),
        # Q10
        ("இரண்டு தொடர்வண்டிகளின் வேக விகிதம் 4:5. மெதுவான தொடர்வண்டி 180 கி.மீ தூரத்தை 4.5 மணி நேரத்தில் கடந்தால், வேகமான தொடர்வண்டியின் வேகத்தைக் காண்க.",
         ["45 கி.மீ/மணி", "50 கி.மீ/மணி", "55 கி.மீ/மணி", "60 கி.மீ/மணி"], 1,
         "மெதுவான தொடர்வண்டியின் வேகம் = 180/4.5 = 40 கி.மீ/மணி. வேக விகிதம்: வேகமானது/மெதுவானது = 5/4. வேகமான தொடர்வண்டியின் வேகம் = (5/4) × 40 = 50 கி.மீ/மணி. முக்கியக் கற்றல் கருத்து: தெரிந்த வேகத்தைப் பெறத் தூரத்தைக் காலத்தால் வகுத்து, பின்னர் விகிதத்தைப் பயன்படுத்தி மற்றொரு வேகத்தைக் காணவும்.", "EASY"),
        # Q11
        ("A ஒரு வேலையை 20 நாட்களிலும், B அதே வேலையை 30 நாட்களிலும் முடிக்க முடியும். இருவரும் சேர்ந்து வேலை செய்தால், அவ்வேலை எத்தனை நாட்களில் முடியும்?",
         ["10 நாட்கள்", "11 நாட்கள்", "12 நாட்கள்", "13 நாட்கள்"], 2,
         "A-இன் 1 நாள் வேலை = 1/20; B-இன் 1 நாள் வேலை = 1/30. ஒருங்கிணைந்த 1 நாள் வேலை = 1/20 + 1/30 = 3/60 + 2/60 = 5/60 = 1/12. இருவரும் சேர்ந்து எடுக்கும் காலம் = 12 நாட்கள். முக்கியக் கற்றல் கருத்து: இரண்டு பணியாளர்களின் ஒருங்கிணைந்த வேலை வீதம் அவர்களின் தனி வீதங்களின் கூடுதலாகும்; தனிக் காலங்களின் சராசரி அல்ல.", "EASY"),
        # Q12
        ("இரண்டு எண்கள் 7:9 என்ற விகிதத்தில் உள்ளன. ஒவ்வோர் எண்ணுடனும் 6 கூட்டினால், விகிதம் 9:11 ஆகிறது. அவ்வெண்களைக் காண்க.",
         ["14 மற்றும் 18", "21 மற்றும் 27", "28 மற்றும் 36", "35 மற்றும் 45"], 1,
         "எண்கள் 7x மற்றும் 9x என்க. (7x + 6)/(9x + 6) = 9/11. 11(7x + 6) = 9(9x + 6) ⟹ 77x + 66 = 81x + 54 ⟹ 4x = 12 ⟹ x = 3. எண்கள் = 7(3) = 21 மற்றும் 9(3) = 27. முக்கியக் கற்றல் கருத்து: ஒரு விகிதத்தின் இரண்டு உறுப்புகளுடனும் ஒரு நிலையான மதிப்பு கூட்டப்படும்போது, புதிய விகிதத்தைக் கொண்டு ஒரு சமன்பாட்டை அமைத்துப் பெருக்கியைக் காணவும்.", "MEDIUM"),
        # Q13
        ("இரண்டு எண்களின் கூடுதல் 350. ஒவ்வோர் எண்ணுடனும் 20 கூட்டினால், புதிய எண்களின் விகிதம் 6:7 ஆகிறது. அவ்விரண்டு எண்களைக் காண்க.",
         ["150 மற்றும் 180", "155 மற்றும் 185", "160 மற்றும் 190", "165 மற்றும் 195"], 2,
         "a + b = 350. ஒவ்வொன்றுடனும் 20 கூட்டிய பின்: (a+20) + (b+20) = 390. 390-ஐ 6:7 என்ற விகிதத்தில் பிரிக்க: a+20 = 180, b+20 = 210. எனவே a = 160 மற்றும் b = 190. முக்கியக் கற்றல் கருத்து: இக்கணக்கு இரண்டு விகிதத் திறன்களை இணைக்கிறது: கூட்டப்பட்ட மாறிலிக்கேற்ப மொத்தக் கூடுதலைச் சரிசெய்தல், பின்னர் புதிய விகிதத்தில் பிரித்தல்.", "MEDIUM"),
        # Q14
        ("இரண்டு எண்கள் 7:9 என்ற விகிதத்தில் உள்ளன. அவற்றின் வர்க்கங்களின் கூடுதல் 1,170 எனில், பெரிய எண்ணைக் காண்க.",
         ["21", "24", "27", "30"], 2,
         "எண்கள் 7k மற்றும் 9k என்க. 49k² + 81k² = 1170 ⟹ 130k² = 1170 ⟹ k² = 9 ⟹ k = 3. பெரிய எண் = 9k = 9 × 3 = 27. முக்கியக் கற்றல் கருத்து: விகித மடங்குகளைக் கொண்டு வர்க்கக் கூடுதல் சமன்பாட்டை அமைத்து, தேவையான எண்ணைக் காணும் முன் k-ஐக் காணவும்.", "MEDIUM"),
        # Q15
        ("நாளொன்றுக்கு 6 மணி நேரம் வேலை செய்யும் 10 பணியாளர்கள் மொத்தம் ₹7,200 ஈட்டினால், அதே வீதத்தில் நாளொன்றுக்கு 8 மணி நேரம் வேலை செய்யும் 15 பணியாளர்கள் எவ்வளவு ஈட்டுவர்?",
         ["₹13,200", "₹13,800", "₹14,400", "₹15,000"], 2,
         "ஒரு பணியாளர்-மணிக்கான வீதம் = 7200 / (10 × 6) = ₹120. புதிய வருவாய் = 120 × (15 × 8) = ₹14,400. முக்கியக் கற்றல் கருத்து: ஓர் அளவு ஒரே நேரத்தில் இரண்டு மாறிகளைச் சார்ந்திருக்கும்போது, புதிய மதிப்புகளுக்குப் பயன்படுத்தும் முன் ஒரே ஒருங்கிணைந்த வீதத்தைக் கணக்கிடவும்.", "MEDIUM"),
        # Q16
        ("₹1,200-ஐ இருவருக்கு 5:7 என்ற விகிதத்தில் பிரிக்கவும்.",
         ["₹450 மற்றும் ₹750", "₹500 மற்றும் ₹700", "₹520 மற்றும் ₹680", "₹480 மற்றும் ₹720"], 1,
         "மொத்தப் பகுதிகள் = 5 + 7 = 12. முதல் பங்கு = (5/12) × 1200 = ₹500. இரண்டாம் பங்கு = (7/12) × 1200 = ₹700. முக்கியக் கற்றல் கருத்து: ஒவ்வொரு பகுதியாலும் பெருக்கும் முன், மொத்தத்தை விகிதப் பகுதிகளின் கூடுதலால் வகுக்கவும்.", "EASY"),
        # Q17
        ("இரண்டு சகோதரர்களின் தற்போதைய வயதுகள் 5:7 என்ற விகிதத்தில் உள்ளன. 6 ஆண்டுகளுக்குப் பின் அவர்களின் வயது விகிதம் 4:5 ஆக இருக்கும். அவர்களின் தற்போதைய வயதுகளைக் காண்க.",
         ["8 மற்றும் 12 ஆண்டுகள்", "10 மற்றும் 14 ஆண்டுகள்", "12 மற்றும் 16 ஆண்டுகள்", "14 மற்றும் 18 ஆண்டுகள்"], 1,
         "தற்போதைய வயதுகள் 5x மற்றும் 7x என்க. (5x + 6)/(7x + 6) = 4/5. 5(5x + 6) = 4(7x + 6) ⟹ 25x + 30 = 28x + 24 ⟹ x = 2. தற்போதைய வயதுகள் = 5(2) = 10 ஆண்டுகள் மற்றும் 7(2) = 14 ஆண்டுகள். முக்கியக் கற்றல் கருத்து: x-ஐக் காணும் முன், 'n ஆண்டுகளுக்குப் பின்' என்ற நிபந்தனையைப் புதிய விகிதத்துடன் ஒரு சமன்பாடாக மாற்றவும்.", "MEDIUM"),
        # Q18
        ("ஒரு பையில் ₹1, 50 பைசா, 25 பைசா நாணயங்கள் 3:4:5 என்ற விகிதத்தில் உள்ளன. நாணயங்களின் மொத்த மதிப்பு ₹500 எனில், 25 பைசா நாணயங்களின் எண்ணிக்கையைக் காண்க.",
         ["350", "380", "400", "420"], 2,
         "நாணயங்கள் 3x, 4x, 5x என்க. மதிப்பு = 3x(1) + 4x(0.5) + 5x(0.25) = 3x + 2x + 1.25x = 6.25x. 6.25x = 500 ⟹ x = 80. 25 பைசா நாணயங்களின் எண்ணிக்கை = 5x = 400. முக்கியக் கற்றல் கருத்து: நாணயங்களின் எண்ணிக்கை விகிதம் மதிப்பு விகிதத்திலிருந்து வேறுபடுவதால், கூட்டும் முன் ஒவ்வொரு வகை நாணயத்தின் எண்ணிக்கையையும் அதன் ரூபாய் மதிப்பாக மாற்றவும்.", "MEDIUM"),
        # Q19
        ("ஒரு கொள்கலனில் 27 லிட்டர் தூய பால் உள்ளது. கலவையில் மூன்றில் ஒரு பங்கு எடுக்கப்பட்டு, தண்ணீரால் நிரப்பப்படுகிறது. கொள்கலனில் மீதமுள்ள பாலின் அளவைக் காண்க.",
         ["16 லிட்டர்", "17 லிட்டர்", "18 லிட்டர்", "19 லிட்டர்"], 2,
         "எடுக்கப்பட்ட பின்னம் = 1/3; மீதமுள்ள பின்னம் = 2/3. மீதமுள்ள பால் = 27 × (2/3) = 18 லிட்டர். முக்கியக் கற்றல் கருத்து: ஒரு முறை மாற்றீடு செய்யும்போது, பாலின் அளவு மீதமுள்ள பின்னத்தால் பெருக்கப்படுகிறது.", "EASY"),
        # Q20
        ("ஒரு பையில் ₹1, 50 பைசா, 25 பைசா நாணயங்கள் 5:6:8 என்ற விகிதத்தில் உள்ளன. நாணயங்களின் மொத்த மதிப்பு ₹210 எனில், 25 பைசா நாணயங்களின் எண்ணிக்கையைக் காண்க.",
         ["144", "156", "168", "180"], 2,
         "நாணயங்களின் எண்ணிக்கை 5x, 6x, 8x என்க. மதிப்பு = 5x(1) + 6x(0.5) + 8x(0.25) = 5x + 3x + 2x = 10x. 10x = 210 ⟹ x = 21. 25 பைசா நாணயங்களின் எண்ணிக்கை = 8x = 168. முக்கியக் கற்றல் கருத்து: வெவ்வேறு மதிப்புள்ள நாணயங்கள் விகிதத்தில் வரும்போது, கூட்டும் முன் ஒவ்வொரு வகையின் எண்ணிக்கையையும் அதன் மதிப்பாக மாற்றவும்.", "MEDIUM"),
        # Q21
        ("இரண்டு எண்கள் 5:6 என்ற விகிதத்தில் உள்ளன. ஒவ்வொன்றிலிருந்தும் 8 கழித்தால், விகிதம் 4:5 ஆகிறது. அவ்வெண்களைக் காண்க.",
         ["30 மற்றும் 36", "35 மற்றும் 42", "40 மற்றும் 48", "45 மற்றும் 54"], 2,
         "எண்கள் 5x மற்றும் 6x என்க. (5x − 8)/(6x − 8) = 4/5. 5(5x − 8) = 4(6x − 8) ⟹ 25x − 40 = 24x − 32 ⟹ x = 8. எண்கள் = 5(8) = 40 மற்றும் 6(8) = 48. முக்கியக் கற்றல் கருத்து: இரண்டு உறுப்புகளிலிருந்தும் ஒரு நிலையான மதிப்பு கழிக்கப்படும்போது, புதிய விகிதத்துடன் ஒரு சமன்பாட்டை அமைத்து x-ஐக் காணவும்.", "MEDIUM"),
        # Q22
        ("84:126 என்ற விகிதத்தைச் சுருக்குக.",
         ["1:2", "2:3", "3:4", "4:5"], 1,
         "விகிதம் = 84 : 126. 84 மற்றும் 126-இன் மீ.பொ.வ = 42. 84 ÷ 42 : 126 ÷ 42 = 2 : 3. முக்கியக் கற்றல் கருத்து: ஒரு விகிதத்தை எளிய வடிவில் எழுத, அதன் இரண்டு உறுப்புகளையும் அவற்றின் மீ.பொ.வ-ஆல் எப்போதும் வகுக்கவும்.", "EASY"),
        # Q23
        ("மூன்று எண்கள் தொடர் விகிதசமத்தில் உள்ளன. முதல் எண் 16, மூன்றாம் எண் 25 எனில், மூன்று எண்களின் கூடுதலைக் காண்க.",
         ["59", "60", "61", "62"], 2,
         "b² = a × c = 16 × 25 = 400 ⟹ b = 20. கூடுதல் = 16 + 20 + 25 = 61. முக்கியக் கற்றல் கருத்து: போட்டித் தேர்வு மதிப்புகள் பொதுவாக முழு எண் விடைகள் வருமாறு அமைக்கப்படுவதால், கண்ட இடை விகிதசம உறுப்பு முழு எண்ணா எனத் தொடர்வதற்கு முன் எப்போதும் சரிபார்க்கவும்.", "MEDIUM"),
        # Q24
        ("32 லிட்டர் கலவையில் பாலும் தண்ணீரும் 3:1 என்ற விகிதத்தில் உள்ளன. பால் : தண்ணீர் விகிதத்தை 3:2 ஆக்க எவ்வளவு தண்ணீர் சேர்க்க வேண்டும்?",
         ["6 லிட்டர்", "7 லிட்டர்", "8 லிட்டர்", "9 லிட்டர்"], 2,
         "பால் = (3/4) × 32 = 24 லிட்டர்; தண்ணீர் = (1/4) × 32 = 8 லிட்டர். பால்: தண்ணீர் = 3 : 2 ஆக, தேவையான தண்ணீர் = 24 × (2/3) = 16 லிட்டர். சேர்க்க வேண்டிய தண்ணீர் = 16 − 8 = 8 லிட்டர். முக்கியக் கற்றல் கருத்து: முதலில் மாறாத அளவை (பால்) கண்டறிந்து, பின்னர் இலக்கு விகிதத்தைப் பயன்படுத்தித் தேவையான தண்ணீரைக்காணவும்.", "MEDIUM"),
        # Q25
        ("A, B, C ஆகியோர் முறையே ₹2,000, ₹3,000, ₹4,000 முதலீட்டுடன் ஒரு வியாபாரத்தைத் தொடங்குகின்றனர். A மற்றும் B 12 மாதங்களுக்கும், C 9 மாதங்களுக்கும் முதலீடு செய்கின்றனர். மொத்த இலாபம் ₹7,000 எனில், A-இன் பங்கைக் காண்க.",
         ["₹1,500", "₹1,750", "₹2,000", "₹2,250"], 1,
         "முதலீடு × காலம்: A = 2000 × 12 = 24,000; B = 3000 × 12 = 36,000; C = 4000 × 9 = 36,000. விகிதம் = 24,000 : 36,000 : 36,000 = 2 : 3 : 3. மொத்தப் பகுதிகள் = 8; A-இன் பங்கு = (2/8) × 7000 = ₹1,750. முக்கியக் கற்றல் கருத்து: ஒருங்கிணைந்த விகிதத்தை அமைக்கும் முன், ஒவ்வொரு கூட்டாளியின் முதலீடு × காலம் பெருக்கற்பலனையும் தனித்தனியாகக் கணக்கிடவும்.", "MEDIUM")
    ]

    # 30 Independent Practice (English)
    indep_en = [
        # Q1
        ("The speeds of two trains are in the ratio 3:4. If the faster train covers 240 km in 3 hours, find the speed of the slower train.",
         ["50 km/h", "55 km/h", "60 km/h", "65 km/h"], 2,
         "Speed of faster train = 240/3 = 80 km/h. Speed ratio: slower/faster = 3/4. Speed of slower train = (3/4) × 80 = 60 km/h. Key Learning Point: Find the actual value of one quantity first, then use the ratio to find the other.", "EASY"),
        # Q2
        ("A mixture of 40 litres contains milk and water in the ratio 4:1. How much water must be added to make the ratio of milk to water 2:1?",
         ["4 litres", "6 litres", "8 litres", "10 litres"], 2,
         "Milk = (4/5) × 40 = 32 litres; Water = (1/5) × 40 = 8 litres. For milk : water = 2 : 1, water required = 32/2 = 16 litres. Water to be added = 16 − 8 = 8 litres. Key Learning Point: When water is added, only the quantity of water changes; the quantity of milk remains constant.", "MEDIUM"),
        # Q3
        ("Two numbers are in the ratio 3:5. If each is increased by 10, the ratio becomes 5:7. Find the numbers.",
         ["12 and 20", "15 and 25", "18 and 30", "21 and 35"], 1,
         "Let the numbers be 3x and 5x. (3x + 10)/(5x + 10) = 5/7. 7(3x + 10) = 5(5x + 10) ⟹ 21x + 70 = 25x + 50 ⟹ x = 5. Numbers = 3(5) = 15 and 5(5) = 25. Key Learning Point: Form an equation from the changed ratio and solve for the multiplier x.", "MEDIUM"),
        # Q4
        ("Three numbers are in continued proportion. If the first number is 4 and the third is 9, find the sum of all three numbers.",
         ["17", "18", "19", "20"], 2,
         "For numbers in continued proportion, a : b = b : c, so b² = a × c. b² = 4 × 9 = 36 ⟹ b = 6. Sum = 4 + 6 + 9 = 19. Key Learning Point: In a continued proportion a:b:c, the middle term b is the mean proportional of a and c, i.e., b = √(a × c).", "MEDIUM"),
        # Q5
        ("Find the third proportional to 6 and 12.",
         ["18", "20", "22", "24"], 3,
         "6 : 12 :: 12 : x. 6x = 12 × 12 ⟹ x = 144/6 = 24. Key Learning Point: Third proportional of a, b is b²/a.", "EASY"),
        # Q6
        ("8 men or 12 women can complete a piece of work in the same number of days. Find the ratio of the efficiency of one man to one woman.",
         ["2:3", "3:2", "4:3", "3:4"], 1,
         "Since 8 men and 12 women do the same work in equal time, their total efforts are equal. 8 × (man's efficiency) = 12 × (woman's efficiency). Man's efficiency: Woman's efficiency = 12 : 8 = 3 : 2. Key Learning Point: Fewer workers taking the same time as more workers implies each of the fewer workers is proportionately more efficient.", "EASY"),
        # Q7
        ("The present ages of two brothers are in the ratio 4:5. After 8 years, the ratio of their ages will be 6:7. Find their present ages.",
         ["12 and 15 years", "16 and 20 years", "20 and 25 years", "24 and 30 years"], 1,
         "Let present ages be 4x and 5x. (4x + 8)/(5x + 8) = 6/7. 7(4x + 8) = 6(5x + 8) ⟹ 28x + 56 = 30x + 48 ⟹ x = 4. Present ages = 4(4) = 16 years and 5(4) = 20 years. Key Learning Point: For 'ratio changes after n years' problems, add n to each ratio multiple and equate to the new ratio.", "MEDIUM"),
        # Q8
        ("If x:y = 2:3 and y:z = 4:5, find x:y:z.",
         ["8:12:15", "2:3:5", "6:9:10", "4:6:9"], 0,
         "x:y = 2:3 = 8:12 (multiplying by 4). y:z = 4:5 = 12:15 (multiplying by 3). x:y:z = 8:12:15. Key Learning Point: Scale each ratio so the shared term (y) matches before combining into a single three-term ratio.", "EASY"),
        # Q9
        ("A can complete a piece of work in 12 days and B can complete the same work in 18 days. If they work together, in how many days will the work be completed?",
         ["6.5 days", "7.0 days", "7.2 days", "7.5 days"], 2,
         "A's 1-day work = 1/12; B's 1-day work = 1/18. Combined 1-day work = 1/12 + 1/18 = 3/36 + 2/36 = 5/36. Time taken together = 36/5 = 7.2 days. Key Learning Point: Add the individual work rates (fractions of work per day), then take the reciprocal of the sum to find the combined time.", "EASY"),
        # Q10
        ("The ratio of the incomes of A and B is 3:2. A's income increases by 25% and B's income increases by 20%. Find the new ratio of their incomes.",
         ["15:8", "20:13", "25:16", "30:19"], 2,
         "New income of A = 3 × (5/4) = 15/4. New income of B = 2 × (6/5) = 12/5. New ratio = 15/4 : 12/5 = 75/20 : 48/20 = 75 : 48 = 25 : 16. Key Learning Point: When each quantity in a ratio changes by a different percentage, multiply each term by its own growth factor before re-simplifying.", "MEDIUM"),
        # Q11
        ("Two numbers are in the ratio 7:9. If their HCF is 5, find the sum of the two numbers.",
         ["70", "75", "80", "85"], 2,
         "The numbers are 7 × 5 = 35 and 9 × 5 = 45. Sum = 35 + 45 = 80. Key Learning Point: Once the HCF is known, multiply each ratio term by it to recover the actual numbers.", "EASY"),
        # Q12
        ("A container has 32 litres of pure milk. 8 litres are withdrawn and replaced with water; the same process is repeated once more. Find the quantity of milk left in the container.",
         ["16 litres", "18 litres", "20 litres", "22 litres"], 1,
         "Fraction removed each time = 8/32 = 1/4; fraction remaining each time = 3/4. After two operations, milk left = 32 × (3/4) × (3/4) = 32 × 9/16 = 18 litres. Key Learning Point: For repeated replacement problems, multiply the initial quantity by the 'fraction remaining' raised to the power of the number of operations.", "MEDIUM"),
        # Q13
        ("Two numbers are in the ratio 9:13. If their HCF is 4, find their LCM.",
         ["432", "450", "468", "486"], 2,
         "Since 9 and 13 are co-prime, the numbers are 9 × 4 = 36 and 13 × 4 = 52. For co-prime ratio terms, LCM = (product of ratio terms) × HCF. LCM = 9 × 13 × 4 = 468. Key Learning Point: For two numbers in a co-prime ratio a:b, LCM = a × b × HCF.", "MEDIUM"),
        # Q14
        ("A invests ₹4,000 for 8 months and B invests ₹6,000 for 6 months in a business. If the total profit is ₹6,800, find B's share.",
         ["₹3,200", "₹3,400", "₹3,600", "₹3,800"], 2,
         "Ratio of investment-months: A = 4000 × 8 = 32,000; B = 6000 × 6 = 36,000. Ratio = 32,000 : 36,000 = 8 : 9. B's share = (9/17) × 6800 = ₹3,600. Key Learning Point: When investment periods differ, profit is shared in the ratio of (capital × time), not capital alone.", "MEDIUM"),
        # Q15
        ("A bag contains ₹5, ₹2, and ₹1 coins in the ratio 3:4:5. If the total value of the coins is ₹840, find the number of ₹2 coins.",
         ["100", "110", "120", "130"], 2,
         "Let the number of coins be 3x, 4x, and 5x. Value = 3x(5) + 4x(2) + 5x(1) = 15x + 8x + 5x = 28x. 28x = 840 ⟹ x = 30. Number of ₹2 coins = 4x = 120. Key Learning Point: Multiply the count of each coin type by its denomination before adding, since ratio of coins is not the same as ratio of value.", "MEDIUM"),
        # Q16
        ("If 6 workers working 8 hours a day earn ₹9,600 in total, how much will 9 workers working 10 hours a day earn, at the same rate?",
         ["₹16,000", "₹17,000", "₹18,000", "₹19,000"], 2,
         "Earnings vary jointly with (number of workers × hours worked). Rate per worker-hour = 9600 / (6 × 8) = ₹200. New earnings = 200 × (9 × 10) = ₹18,000. Key Learning Point: In joint variation problems, find the constant rate per unit of the combined quantity, then scale to the new situation.", "MEDIUM"),
        # Q17
        ("A, B and C start a business with capitals of ₹3,000, ₹4,000 and ₹5,000 respectively. A and B invest for the full 12 months, but C joins after 6 months and invests for only 6 months. If the total profit is ₹4,750, find C's share.",
         ["₹1,150", "₹1,200", "₹1,250", "₹1,300"], 2,
         "Capital-time: A = 3000 × 12 = 36,000; B = 4000 × 12 = 48,000; C = 5000 × 6 = 30,000. Ratio = 36,000 : 48,000 : 30,000 = 6 : 8 : 5. Total parts = 19; C's share = (5/19) × 4750 = ₹1,250. Key Learning Point: When a partner joins later, use only the months that partner's capital was actually invested for.", "MEDIUM"),
        # Q18
        ("A sum of money is divided among A, B and C in the ratio 2:3:5. If C receives ₹450 more than A, find the total sum.",
         ["₹1,200", "₹1,350", "₹1,500", "₹1,650"], 2,
         "Difference between C's and A's parts = 5 − 2 = 3 parts = ₹450. 1 part = ₹150. Total sum = 10 parts = 150 × 10 = ₹1,500. Key Learning Point: Use the difference between two shares' parts to find the value of one part, then scale to the total.", "EASY"),
        # Q19
        ("The sum of two numbers is 160. If 10 is added to each number, the ratio of the new numbers becomes 4:5. Find the two numbers.",
         ["60 and 100", "65 and 95", "70 and 90", "75 and 85"], 2,
         "Let the numbers be a and b, with a + b = 160. After adding 10 to each: (a+10)/(b+10) = 4/5. Since a+b = 160, (a+10)+(b+10) = 180. Splitting 180 in ratio 4:5 gives a+10 = 80, b+10 = 100. So a = 70 and b = 90. Key Learning Point: When the sum is fixed and a constant is added to both numbers, the new sum can be split directly in the new ratio.", "MEDIUM"),
        # Q20
        ("Two numbers are in the ratio 3:4. If their product is 972, find the larger number.",
         ["27", "30", "33", "36"], 3,
         "Let the numbers be 3k and 4k. 3k × 4k = 972 ⟹ 12k² = 972 ⟹ k² = 81 ⟹ k = 9. Larger number = 4k = 4 × 9 = 36. Key Learning Point: When two numbers are given as a ratio along with their product, represent them as multiples of k and solve for k using the product condition.", "MEDIUM"),
        # Q21
        ("Find the mean proportion between 9 and 25.",
         ["12", "14", "15", "17"], 2,
         "Mean proportion = √(9 × 25) = √225 = 15. Key Learning Point: Mean proportion of a, b is √(a × b).", "EASY"),
        # Q22
        ("The sum of two numbers is 495 and they are in the ratio 4:7. Find the larger number.",
         ["280", "300", "315", "330"], 2,
         "Total parts = 4 + 7 = 11. Larger number = (7/11) × 495 = 315. Key Learning Point: For 'sum given' problems, divide the sum by the total number of parts first.", "EASY"),
        # Q23
        ("On a map with a scale of 1:2,00,000, the area of a district is shown as 5 sq. cm. Find the actual area of the district in sq. km. (1 km = 1,00,000 cm)",
         ["15 sq. km", "18 sq. km", "20 sq. km", "24 sq. km"], 2,
         "Linear scale = 1 : 2,00,000, so area scale = 1² : (2,00,000)². Actual area (in cm²) = 5 × (2,00,000)² cm². Converting cm² to km² (1 km² = 10¹⁰ cm²): Actual area = 5 × 4 × 10¹⁰ / 10¹⁰ = 20 sq. km. Key Learning Point: For area, the scale ratio must be squared (duplicate ratio), since area is a two-dimensional quantity.", "MEDIUM"),
        # Q24
        ("Find the duplicate ratio of 5:7.",
         ["10:14", "25:49", "5:49", "25:7"], 1,
         "Duplicate ratio of 5:7 = 5² : 7² = 25 : 49. Key Learning Point: Duplicate ratio means squaring each term of the ratio.", "EASY"),
        # Q25
        ("Simplify the ratio 96:144.",
         ["1:2", "2:3", "3:4", "4:5"], 1,
         "HCF of 96 and 144 = 48. 96 ÷ 48 : 144 ÷ 48 = 2 : 3. Key Learning Point: Divide both terms by their HCF to simplify a ratio.", "EASY"),
        # Q26
        ("Two numbers are in the ratio 8:11. If each number is decreased by 4, the ratio becomes 5:7. Find the numbers.",
         ["48 and 66", "56 and 77", "64 and 88", "72 and 99"], 2,
         "Let the numbers be 8x and 11x. (8x − 4)/(11x − 4) = 5/7. 7(8x − 4) = 5(11x − 4) ⟹ 56x − 28 = 55x − 20 ⟹ x = 8. Numbers = 8(8) = 64 and 11(8) = 88. Key Learning Point: Form an equation from the changed ratio and solve for the multiplier x, then substitute back to find the actual numbers.", "MEDIUM"),
        # Q27
        ("In a survey of 700 people, the number who prefer tea only, coffee only, both, and neither are in the ratio 5:4:3:2. Find the number of people who prefer both tea and coffee.",
         ["100", "125", "150", "175"], 2,
         "Total parts = 5 + 4 + 3 + 2 = 14. Value of 1 part = 700/14 = 50. People who prefer both = 3 parts = 3 × 50 = 150. Key Learning Point: When a total is split into several named categories by ratio, find the value of one part before extracting any single category.", "MEDIUM"),
        # Q28
        ("Divide ₹980 between two people in the ratio 3:4.",
         ["₹400 and ₹580", "₹420 and ₹560", "₹440 and ₹540", "₹450 and ₹530"], 1,
         "Total parts = 3 + 4 = 7. First share = (3/7) × 980 = ₹420. Second share = (4/7) × 980 = ₹560. Key Learning Point: Divide the total quantity by the sum of the parts first.", "EASY"),
        # Q29
        ("If A:B = 3:4 and B:C = 5:6, find A:B:C.",
         ["15:20:24", "3:4:6", "9:12:18", "6:8:10"], 0,
         "A:B = 3:4 = 15:20 (multiplying by 5). B:C = 5:6 = 20:24 (multiplying by 4). A:B:C = 15:20:24. Key Learning Point: To combine two ratios, make the common term (B) equal in both before joining them.", "EASY"),
        # Q30
        ("Two numbers are in the ratio 5:4. If the sum of their squares is 1,476, find the larger number.",
         ["24", "28", "30", "32"], 2,
         "Let the numbers be 5k and 4k. (5k)² + (4k)² = 1476 ⟹ 25k² + 16k² = 1476 ⟹ 41k² = 1476 ⟹ k² = 36 ⟹ k = 6. Larger number = 5k = 5 × 6 = 30. Key Learning Point: When numbers are given as a ratio, represent them as multiples of a common variable before applying the given condition.", "MEDIUM")
    ]

    # 30 Independent Practice (Tamil)
    indep_ta = [
        # Q1
        ("இரண்டு தொடர்வண்டிகளின் வேக விகிதம் 3:4. வேகமான தொடர்வண்டி 240 கி.மீ தூரத்தை 3 மணி நேரத்தில் கடந்தால், மெதுவான தொடர்வண்டியின் வேகத்தைக் காண்க.",
         ["50 கி.மீ/மணி", "55 கி.மீ/மணி", "60 கி.மீ/மணி", "65 கி.மீ/மணி"], 2,
         "வேகமான தொடர்வண்டியின் வேகம் = 240/3 = 80 கி.மீ/மணி. வேக விகிதம்: மெதுவானது/வேகமானது = 3/4. மெதுவான தொடர்வண்டியின் வேகம் = (3/4) × 80 = 60 கி.மீ/மணி. முக்கியக் கற்றல் கருத்து: முதலில் ஓர் அளவின் உண்மையான மதிப்பைக் கண்டறிந்து, பின்னர் விகிதத்தைப் பயன்படுத்தி மற்றொன்றைக் காணவும்.", "EASY"),
        # Q2
        ("40 லிட்டர் கலவையில் பாலும் தண்ணீரும் 4:1 என்ற விகிதத்தில் உள்ளன. பால் : தண்ணீர் விகிதத்தை 2:1 ஆக்க எவ்வளவு தண்ணீர் சேர்க்க வேண்டும்?",
         ["4 லிட்டர்", "6 லிட்டர்", "8 லிட்டர்", "10 லிட்டர்"], 2,
         "பால் = (4/5) × 40 = 32 லிட்டர்; தண்ணீர் = (1/5) × 40 = 8 லிட்டர். பால்: தண்ணீர் = 2 : 1 ஆக, தேவையான தண்ணீர் = 32/2 = 16 லிட்டர். சேர்க்க வேண்டிய தண்ணீர் = 16 − 8 = 8 லிட்டர். முக்கியக் கற்றல் கருத்து: தண்ணீர் சேர்க்கப்படும்போது, தண்ணீரின் அளவு மட்டுமே மாறுகிறது; பாலின் அளவு மாறாமல் இருக்கும்.", "MEDIUM"),
        # Q3
        ("இரண்டு எண்கள் 3:5 என்ற விகிதத்தில் உள்ளன. ஒவ்வொன்றுடனும் 10 கூட்டினால், விகிதம் 5:7 ஆகிறது. அவ்வெண்களைக் காண்க.",
         ["12 மற்றும் 20", "15 மற்றும் 25", "18 மற்றும் 30", "21 மற்றும் 35"], 1,
         "எண்கள் 3x மற்றும் 5x என்க. (3x + 10)/(5x + 10) = 5/7. 7(3x + 10) = 5(5x + 10) ⟹ 21x + 70 = 25x + 50 ⟹ x = 5. எண்கள் = 3(5) = 15 மற்றும் 5(5) = 25. முக்கியக் கற்றல் கருத்து: மாறிய விகிதத்திலிருந்து ஒரு சமன்பாட்டை அமைத்துப் பெருக்கி x-ஐக் காணவும்.", "MEDIUM"),
        # Q4
        ("மூன்று எண்கள் தொடர் விகிதசமத்தில் உள்ளன. முதல் எண் 4, மூன்றாம் எண் 9 எனில், மூன்று எண்களின் கூடுதலைக் காண்க.",
         ["17", "18", "19", "20"], 2,
         "தொடர் விகிதசமத்தில் உள்ள எண்களுக்கு a : b = b : c, எனவே b² = a × c. b² = 4 × 9 = 36 ⟹ b = 6. கூடுதல் = 4 + 6 + 9 = 19. முக்கியக் கற்றல் கருத்து: a:b:c என்ற தொடர் விகிதசமத்தில், நடு உறுப்பு b என்பது a மற்றும் c-இன் இடை விகிதசம உறுப்பு; அதாவது b = √(a × c).", "MEDIUM"),
        # Q5
        ("6 மற்றும் 12-இன் மூன்றாம் விகிதசம உறுப்பைக் காண்க.",
         ["18", "20", "22", "24"], 3,
         "6 : 12 :: 12 : x. 6x = 12 × 12 ⟹ x = 144/6 = 24. முக்கியக் கற்றல் கருத்து: a, b-இன் மூன்றாம் விகிதசம உறுப்பு b²/a ஆகும்.", "EASY"),
        # Q6
        ("8 ஆண்கள் அல்லது 12 பெண்கள் ஒரு வேலையை ஒரே எண்ணிக்கையிலான நாட்களில் முடிக்க முடியும். ஓர் ஆணுக்கும் ஒரு பெண்ணுக்கும் இடையிலான திறன் விகிதத்தைக் காண்க.",
         ["2:3", "3:2", "4:3", "3:4"], 1,
         "8 ஆண்களும் 12 பெண்களும் ஒரே வேலையைச் சம காலத்தில் செய்வதால், அவர்களின் மொத்த உழைப்பு சமம். 8 × (ஆணின் திறன்) = 12 × (பெண்ணின் திறன்). ஆணின் திறன் : பெண்ணின் திறன் = 12 : 8 = 3 : 2. முக்கியக் கற்றல் கருத்து: குறைவான பணியாளர்கள் அதிகமான பணியாளர்களின் அதே காலத்தை எடுத்துக்கொண்டால், குறைவான பணியாளர்களில் ஒவ்வொருவரும் விகிதாசாரமாக அதிகத் திறன் உடையவர் என்பது பொருள்.", "EASY"),
        # Q7
        ("இரண்டு சகோதரர்களின் தற்போதைய வயதுகள் 4:5 என்ற விகிதத்தில் உள்ளன. 8 ஆண்டுகளுக்குப் பின் அவர்களின் வயது விகிதம் 6:7 ஆக இருக்கும். அவர்களின் தற்போதைய வயதுகளைக் காண்க.",
         ["12 மற்றும் 15 ஆண்டுகள்", "16 மற்றும் 20 ஆண்டுகள்", "20 மற்றும் 25 ஆண்டுகள்", "24 மற்றும் 30 ஆண்டுகள்"], 1,
         "தற்போதைய வயதுகள் 4x மற்றும் 5x என்க. (4x + 8)/(5x + 8) = 6/7. 7(4x + 8) = 6(5x + 8) ⟹ 28x + 56 = 30x + 48 ⟹ x = 4. தற்போதைய வயதுகள் = 4(4) = 16 ஆண்டுகள் மற்றும் 5(4) = 20 ஆண்டுகள். முக்கியக் கற்றல் கருத்து: 'n ஆண்டுகளுக்குப் பின் விகிதம் மாறும்' கணக்குகளில், ஒவ்வொரு விகித மடங்குடனும் n-ஐக் கூட்டிப் புதிய விகிதத்துடன் சமப்படுத்தவும்.", "MEDIUM"),
        # Q8
        ("x:y = 2:3 மற்றும் y:z = 4:5 எனில், x:y:z-ஐக் காண்க.",
         ["8:12:15", "2:3:5", "6:9:10", "4:6:9"], 0,
         "x:y = 2:3 = 8:12 (4-ஆல் பெருக்க). y:z = 4:5 = 12:15 (3-ஆல் பெருக்க). x:y:z = 8:12:15. முக்கியக் கற்றல் கருத்து: ஒரே மூன்று-உறுப்பு விகிதமாக இணைக்கும் முன், பொது உறுப்பு (y) பொருந்துமாறு ஒவ்வொரு விகிதத்தையும் மாற்றியமைக்கவும்.", "EASY"),
        # Q9
        ("A ஒரு வேலையை 12 நாட்களிலும், B அதே வேலையை 18 நாட்களிலும் முடிக்க முடியும். இருவரும் சேர்ந்து வேலை செய்தால், அவ்வேலை எத்தனை நாட்களில் முடியும்?",
         ["6.5 நாட்கள்", "7.0 நாட்கள்", "7.2 நாட்கள்", "7.5 நாட்கள்"], 2,
         "A-இன் 1 நாள் வேலை = 1/12; B-இன் 1 நாள் வேலை = 1/18. ஒருங்கிணைந்த 1 நாள் வேலை = 1/12 + 1/18 = 3/36 + 2/36 = 5/36. இருவரும் சேர்ந்து எடுக்கும் காலம் = 36/5 = 7.2 நாட்கள். முக்கியக் கற்றல் கருத்து: தனி வேலை வீதங்களை (நாளொன்றுக்கான வேலைப் பின்னங்கள்) கூட்டி, அக்கூடுதலின் தலைகீழியை எடுத்து ஒருங்கிணைந்த காலத்தைக் காணவும்.", "EASY"),
        # Q10
        ("A மற்றும் B-இன் வருமான விகிதம் 3:2. A-இன் வருமானம் 25%, B-இன் வருமானம் 20% அதிகரிக்கிறது. அவர்களின் வருமானத்தின் புதிய விகிதத்தைக் காண்க.",
         ["15:8", "20:13", "25:16", "30:19"], 2,
         "A-இன் புதிய வருமானம் = 3 × (5/4) = 15/4. B-இன் புதிய வருமானம் = 2 × (6/5) = 12/5. புதிய விகிதம் = 15/4 : 12/5 = 75/20 : 48/20 = 75 : 48 = 25 : 16. முக்கியக் கற்றல் கருத்து: ஒரு விகிதத்தின் ஒவ்வோர் அளவும் வெவ்வேறு சதவீதத்தில் மாறும்போது, மீண்டும் சுருக்கும் முன் ஒவ்வோர் உறுப்பையும் அதன் சொந்த வளர்ச்சிக் காரணியால் பெருக்கவும்.", "MEDIUM"),
        # Q11
        ("இரண்டு எண்கள் 7:9 என்ற விகிதத்தில் உள்ளன. அவற்றின் மீ.பொ.வ 5 எனில், அவ்விரண்டு எண்களின் கூடுதலைக் காண்க.",
         ["70", "75", "80", "85"], 2,
         "எண்கள் 7 × 5 = 35 மற்றும் 9 × 5 = 45. கூடுதல் = 35 + 45 = 80. முக்கியக் கற்றல் கருத்து: மீ.பொ.வ தெரிந்தவுடன், ஒவ்வொரு விகித உறுப்பையும் அதனால் பெருக்கி உண்மையான எண்களைப் பெறவும்.", "EASY"),
        # Q12
        ("ஒரு கொள்கலனில் 32 லிட்டர் தூய பால் உள்ளது. 8 லிட்டர் எடுக்கப்பட்டுத் தண்ணீFormat 8/32 = 1/4; ஒவ்வொரு முறையும் மீதமுள்ள பின்னம் = 3/4. இரண்டு செயல்களுக்குப் பின், மீதமுள்ள பால் = 32 × (3/4) × (3/4) = 32 × 9/16 = 18 லிட்டர்.",
         ["16 லிட்டர்", "18 லிட்டர்", "20 லிட்டர்", "22 லிட்டர்"], 1,
         "ஒவ்வொரு முறையும் எடுக்கப்படும் பின்னம் = 8/32 = 1/4; ஒவ்வொரு முறையும் மீதமுள்ள பின்னம் = 3/4. இரண்டு செயல்களுக்குப் பின், மீதமுள்ள பால் = 32 × (3/4) × (3/4) = 32 × 9/16 = 18 லிட்டர். முக்கியக் கற்றல் கருத்து: தொடர் மாற்றீட்டுக் கணக்குகளில், தொடக்க அளவை 'மீதமுள்ள பின்னத்தின்' செயல்களின் எண்ணிக்கை அடுக்கால் பெருக்கவும்.", "MEDIUM"),
        # Q13
        ("இரண்டு எண்கள் 9:13 என்ற விகிதத்தில் உள்ளன. அவற்றின் மீ.பொ.வ 4 எனில், அவற்றின் மீ.பொ.ம-வைக் காண்க.",
         ["432", "450", "468", "486"], 2,
         "9 மற்றும் 13 சார்பகா எண்கள் என்பதால், எண்கள் 9 × 4 = 36 மற்றும் 13 × 4 = 52. சார்பகா விகித உறுப்புகளுக்கு, மீ.பொ.ம = (விகித உறுப்புகளின் பெருக்கற்பலன்) × மீ.பொ.வ. மீ.பொ.ம = 9 × 13 × 4 = 468. முக்கியக் கற்றல் கருத்து: a:b என்ற சார்பகா விகிதத்திலுள்ள இரண்டு எண்களுக்கு, மீ.பொ.ம = a × b × மீ.பொ.வ.", "MEDIUM"),
        # Q14
        ("ஒரு வியாபாரத்தில் A ₹4,000-ஐ 8 மாதங்களுக்கும், B ₹6,000-ஐ 6 மாதங்களுக்கும் முதலீடு செய்கின்றனர். மொத்த இலாபம் ₹6,800 எனில், B-இன் பங்கைக் காண்க.",
         ["₹3,200", "₹3,400", "₹3,600", "₹3,800"], 2,
         "முதலீடு-மாதங்களின் விகிதம்: A = 4000 × 8 = 32,000; B = 6000 × 6 = 36,000. விகிதம் = 32,000 : 36,000 = 8 : 9. B-இன் பங்கு = (9/17) × 6800 = ₹3,600. முக்கியக் கற்றல் கருத்து: முதலீட்டுக் காலங்கள் வேறுபடும்போது, இலாபம் முதலீட்டின் விகிதத்தில் மட்டும் அல்லாமல் (முதலீடு × காலம்) விகிதத்தில் பகிரப்படுகிறது.", "MEDIUM"),
        # Q15
        ("ஒரு பையில் ₹5, ₹2, ₹1 நாணயங்கள் 3:4:5 என்ற விகிதத்தில் உள்ளன. நாணயங்களின் மொத்த மதிப்பு ₹840 எனில், ₹2 நாணயங்களின் எண்ணிக்கையைக் காண்க.",
         ["100", "110", "120", "130"], 2,
         "நாணயங்களின் எண்ணிக்கை 3x, 4x, 5x என்க. மதிப்பு = 3x(5) + 4x(2) + 5x(1) = 15x + 8x + 5x = 28x. 28x = 840 ⟹ x = 30. ₹2 நாணயங்களின் எண்ணிக்கை = 4x = 120. முக்கியக் கற்றல் கருத்து: நாணயங்களின் எண்ணிக்கை விகிதமும் மதிப்பு விகிதமும் ஒன்றல்ல; எனவே கூட்டும் முன் ஒவ்வொரு வகை நாணயத்தின் எண்ணிக்கையையும் அதன் மதிப்பால் பெருக்கவும்.", "MEDIUM"),
        # Q16
        ("நாளொன்றுக்கு 8 மணி நேரம் வேலை செய்யும் 6 பணியாளர்கள் மொத்தம் ₹9,600 ஈட்டினால், அதே வீதத்தில் நாளொன்றுக்கு 10 மணி நேரம் வேலை செய்யும் 9 பணியாளர்கள் எவ்வளவு ஈட்டுவர்?",
         ["₹16,000", "₹17,000", "₹18,000", "₹19,000"], 2,
         "வருவாய் (பணியாளர்களின் எண்ணிக்கை × வேலை மணி நேரம்) உடன் கூட்டாக மாறுகிறது. ஒரு பணியாளர்-மணிக்கான வீதம் = 9600 / (6 × 8) = ₹200. புதிய வருவாய் = 200 × (9 × 10) = ₹18,000. முக்கியக் கற்றல் கருத்து: கூட்டு மாறுபாட்டுக் கணக்குகளில், ஒருங்கிணைந்த அளவின் ஓர் அலகுக்கான மாறா வீதத்தைக் கண்டறிந்து, புதிய சூழலுக்கு ஏற்ப மாற்றியமைக்கவும்.", "MEDIUM"),
        # Q17
        ("A, B, C ஆகியோர் முறையே ₹3,000, ₹4,000, ₹5,000 முதலீட்டுடன் ஒரு வியாபாரத்தைத் தொடங்குகின்றனர். A மற்றும் B முழு 12 மாதங்களுக்கும் முதலீடு செய்கின்றனர்; ஆனால் C 6 மாதங்களுக்குப் பின் சேர்ந்து 6 மாதங்களுக்கு மட்டுமே முதலீடு செய்கிறார். மொத்த இலாபம் ₹4,750 எனில், C-இன் பங்கைக் காண்க.",
         ["₹1,150", "₹1,200", "₹1,250", "₹1,300"], 2,
         "முதலீடு × காலம்: A = 3000 × 12 = 36,000; B = 4000 × 12 = 48,000; C = 5000 × 6 = 30,000. விகிதம் = 36,000 : 48,000 : 30,000 = 6 : 8 : 5. மொத்தப் பகுதிகள் = 19; C-இன் பங்கு = (5/19) × 4750 = ₹1,250. முக்கியக் கற்றல் கருத்து: ஒரு கூட்டாளி பின்னர் சேரும்போது, அவரது முதலீடு உண்மையில் இருந்த மாதங்களை மட்டுமே பயன்படுத்தவும்.", "MEDIUM"),
        # Q18
        ("ஒரு தொகை A, B, C ஆகியோருக்கு 2:3:5 என்ற விகிதத்தில் பிரிக்கப்படுகிறது. A-ஐ விட C ₹450 அதிகம் பெற்றால், மொத்தத் தொகையைக் காண்க.",
         ["₹1,200", "₹1,350", "₹1,500", "₹1,650"], 2,
         "C மற்றும் A-இன் பகுதிகளுக்கிடையிலான வேறுபாடு = 5 − 2 = 3 பகுதிகள் = ₹450. 1 பகுதி = ₹150. மொத்தத் தொகை = 10 பகுதிகள் = 150 × 10 = ₹1,500. முக்கியக் கற்றல் கருத்து: இரண்டு பங்குகளின் பகுதிகளுக்கிடையிலான வேறுபாட்டைக் கொண்டு ஒரு பகுதியின் மதிப்பைக் கண்டறிந்து, பின்னர் மொத்தத்திற்கு மாற்றியமைக்கவும்.", "EASY"),
        # Q19
        ("இரண்டு எண்களின் கூடுதல் 160. ஒவ்வோர் எண்ணுடனும் 10 கூட்டினால், புதிய எண்களின் விகிதம் 4:5 ஆகிறது. அவ்விரண்டு எண்களைக் காண்க.",
         ["60 மற்றும் 100", "65 மற்றும் 95", "70 மற்றும் 90", "75 மற்றும் 85"], 2,
         "எண்கள் a மற்றும் b என்க; a + b = 160. ஒவ்வொன்றுடனும் 10 கூட்டிய பின்: (a+10)/(b+10) = 4/5. a+b = 160 என்பதால், (a+10)+(b+10) = 180. 180-ஐ 4:5 என்ற விகிதத்தில் பிரிக்க: a+10 = 80, b+10 = 100. எனவே a = 70 மற்றும் b = 90. முக்கியக் கற்றல் கருத்து: கூடுதல் நிலையாக இருந்து இரண்டு எண்களுடனும் ஒரு மாறிலி கூட்டப்படும்போது, புதிய கூடுதலை நேரடியாகப் புதிய விகிதத்தில் பிரிக்கலாம்.", "MEDIUM"),
        # Q20
        ("இரண்டு எண்கள் 3:4 என்ற விகிதத்தில் உள்ளன. அவற்றின் பெருக்கற்பலன் 972 எனில், பெரிய எண்ணைக் காண்க.",
         ["27", "30", "33", "36"], 3,
         "எண்கள் 3k மற்றும் 4k என்க. 3k × 4k = 972 ⟹ 12k² = 972 ⟹ k² = 81 ⟹ k = 9. பெரிய எண் = 4k = 4 × 9 = 36. முக்கியக் கற்றல் கருத்து: இரண்டு எண்கள் விகிதமாகவும் அவற்றின் பெருக்கற்பலனும் கொடுக்கப்படும்போது, அவற்றை k-இன் மடங்குகளாக எழுதிப் பெருக்கற்பலன் நிபந்தனையைக் கொண்டு k-ஐக் காணவும்.", "MEDIUM"),
        # Q21
        ("9 மற்றும் 25-இன் இடை விகிதசம உறுப்பைக் காண்க.",
         ["12", "14", "15", "17"], 2,
         "இடை விகிதசம உறுப்பு = √(9 × 25) = √225 = 15. முக்கியக் கற்றல் கருத்து: a, b-இன் இடை விகிதசம உறுப்பு √(a × b).", "EASY"),
        # Q22
        ("இரண்டு எண்களின் கூடுதல் 495; அவை 4:7 என்ற விகிதத்தில் உள்ளன. பெரிய எண்ணைக் காண்க.",
         ["280", "300", "315", "330"], 2,
         "மொத்தப் பகுதிகள் = 4 + 7 = 11. பெரிய எண் = (7/11) × 495 = 315. முக்கியக் கற்றல் கருத்து: 'கூடுதல் கொடுக்கப்பட்ட' கணக்குகளில், முதலில் கூடுதலை மொத்தப் பகுதிகளின் எண்ணிக்கையால் வகுக்கவும்.", "EASY"),
        # Q23
        ("1:2,00,000 அளவுகோல் கொண்ட ஒரு வரைபடத்தில், ஒரு மாவட்டத்தின் பரப்பு 5 ச.செ.மீ ஆகக் காட்டப்பட்டுள்ளது. அம்மாவட்டத்தின் உண்மையான பரப்பை ச.கி.மீ-இல் காண்க. (1 கி.மீ = 1,00,000 செ.மீ)",
         ["15 ச.கி.மீ", "18 ச.கி.மீ", "20 ச.கி.மீ", "24 ச.கி.மீ"], 2,
         "நேரியல் அளவுகோல் = 1 : 2,00,000, எனவே பரப்பு அளவுகோல் = 1² : (2,00,000)². உண்மையான பரப்பு (செ.மீ²-இல்) = 5 × (2,00,000)² செ.மீ². செ.மீ²-ஐ கி.மீ²-ஆக மாற்ற (1 கி.மீ² = 10¹⁰ செ.மீ²): உண்மையான பரப்பு = 5 × 4 × 10¹⁰ / 10¹⁰ = 20 ச.கி.மீ. முக்கியக் கற்றல் கருத்து: பரப்பு இருபரிமாண அளவு என்பதால், பரப்புக்கு அளவுகோல் விகிதம் வர்க்கப்படுத்தப்பட வேண்டும் (இருமடி விகிதம்).", "MEDIUM"),
        # Q24
        ("5:7-இன் இருமடி விகிதத்தைக் காண்க.",
         ["10:14", "25:49", "5:49", "25:7"], 1,
         "5:7-இன் இருமடி விகிதம் = 5² : 7² = 25 : 49. முக்கியக் கற்றல் கருத்து: இருமடி விகிதம் என்பது விகிதத்தின் ஒவ்வோர் உறுப்பையும் வர்க்கப்படுத்துவதாகும்.", "EASY"),
        # Q25
        ("96:144 என்ற விகிதத்தைச் சுருக்குக.",
         ["1:2", "2:3", "3:4", "4:5"], 1,
         "96 மற்றும் 144-இன் மீ.பொ.வ = 48. 96 ÷ 48 : 144 ÷ 48 = 2 : 3. முக்கியக் கற்றல் கருத்து: ஒரு விகிதத்தைச் சுருக்க, இரண்டு உறுப்புகளையும் அவற்றின் மீ.பொ.வ-ஆல் வகுக்கவும்.", "EASY"),
        # Q26
        ("இரண்டு எண்கள் 8:11 என்ற விகிதத்தில் உள்ளன. ஒவ்வோர் எண்ணிலிருந்தும் 4 கழித்தால், விகிதம் 5:7 ஆகிறது. அவ்வெண்களைக் காண்க.",
         ["48 மற்றும் 66", "56 மற்றும் 77", "64 மற்றும் 88", "72 மற்றும் 99"], 2,
         "எண்கள் 8x மற்றும் 11x என்க. (8x − 4)/(11x − 4) = 5/7. 7(8x − 4) = 5(11x − 4) ⟹ 56x − 28 = 55x − 20 ⟹ x = 8. எண்கள் = 8(8) = 64 மற்றும் 11(8) = 88. முக்கியக் கற்றல் கருத்து: மாறிய விகிதத்திலிருந்து ஒரு சமன்பாட்டை அமைத்துப் பெருக்கி x-ஐக் கண்டறிந்து, பின்னர் பிரதியிட்டு உண்மையான எண்களைக் காணவும்.", "MEDIUM"),
        # Q27
        ("700 பேரிடம் நடத்தப்பட்ட ஒரு கணக்கெடுப்பில், தேநீர் மட்டும், காபி மட்டும், இரண்டும், எதுவுமில்லை என விரும்புவோரின் எண்ணிக்கை 5:4:3:2 என்ற விகிதத்தில் உள்ளது. தேநீர் மற்றும் காபி இரண்டையும் விரும்புவோரின் எண்ணிக்கையைக் காண்க.",
         ["100", "125", "150", "175"], 2,
         "மொத்தப் பகுதிகள் = 5 + 4 + 3 + 2 = 14. 1 பகுதியின் மதிப்பு = 700/14 = 50. இரண்டையும் விரும்புவோர் = 3 பகுதிகள் = 3 × 50 = 150. முக்கியக் கற்றல் கருத்து: ஒரு மொத்தம் பல பெயரிடப்பட்ட வகைகளாக விகிதப்படி பிரிக்கப்படும்போது, எந்த ஒரு வகையையும் பிரித்தெடுக்கும் முன் ஒரு பகுதியின் மதிப்பைக் கண்டறியவும்.", "MEDIUM"),
        # Q28
        ("₹980-ஐ இருவருக்கு 3:4 என்ற விகிதத்தில் பிரிக்கவும்.",
         ["₹400 மற்றும் ₹580", "₹420 மற்றும் ₹560", "₹440 மற்றும் ₹540", "₹450 மற்றும் ₹530"], 1,
         "மொத்தப் பகுதிகள் = 3 + 4 = 7. முதல் பங்கு = (3/7) × 980 = ₹420. இரண்டாம் பங்கு = (4/7) × 980 = ₹560. முக்கியக் கற்றல் கருத்து: முதலில் மொத்த அளவைப் பகுதிகளின் கூடுதலால் வகுக்கவும்.", "EASY"),
        # Q29
        ("A:B = 3:4 மற்றும் B:C = 5:6 எனில், A:B:C-ஐக் காண்க.",
         ["15:20:24", "3:4:6", "9:12:18", "6:8:10"], 0,
         "A:B = 3:4 = 15:20 (5-ஆல் பெருக்க). B:C = 5:6 = 20:24 (4-ஆல் பெருக்க). A:B:C = 15:20:24. முக்கியக் கற்றல் கருத்து: இரண்டு விகிதங்களை இணைக்க, இணைக்கும் முன் இரண்டிலும் பொது உறுப்பை (B) சமமாக்கவும்.", "EASY"),
        # Q30
        ("இரண்டு எண்கள் 5:4 என்ற விகிதத்தில் உள்ளன. அவற்றின் வர்க்கங்களின் கூடுதல் 1,476 எனில், பெரிய எண்ணைக் காண்க.",
         ["24", "28", "30", "32"], 2,
         "எண்கள் 5k மற்றும் 4k என்க. (5k)² + (4k)² = 1476 ⟹ 25k² + 16k² = 1476 ⟹ 41k² = 1476 ⟹ k² = 36 ⟹ k = 6. பெரிய எண் = 5k = 5 × 6 = 30. முக்கியக் கற்றல் கருத்து: எண்கள் விகிதமாகக் கொடுக்கப்படும்போது, கொடுக்கப்பட்ட நிபந்தனையைப் பயன்படுத்தும் முன் அவற்றை ஒரு பொது மாறியின் மடங்குகளாக எழுதவும்.", "MEDIUM")
    ]

    # 30 Graded Assessment (English)
    graded_en = [
        # Q1
        ("The cost of 25 pens is ₹375. Find the cost of 60 pens at the same rate.",
         ["₹800", "₹850", "₹900", "₹950"], 2,
         "Cost of 1 pen = 375 ÷ 25 = ₹15. Cost of 60 pens = 15 × 60 = ₹900. Key Learning Point: In direct proportion, find the unit value first and then multiply by the required quantity.", "EASY"),
        # Q2
        ("Two numbers are in the ratio 2:3. If each is increased by 6, the ratio becomes 5:7. Find the numbers.",
         ["18 and 27", "20 and 30", "24 and 36", "28 and 42"], 2,
         "Let the numbers be 2x and 3x. (2x + 6)/(3x + 6) = 5/7. 7(2x + 6) = 5(3x + 6) ⟹ 14x + 42 = 15x + 30 ⟹ x = 12. Numbers = 2(12) = 24 and 3(12) = 36. Key Learning Point: When the same value is added to both terms, form an equation with the new ratio and solve for the multiplier.", "MEDIUM"),
        # Q3
        ("A invests ₹5,000 for 12 months and B invests ₹7,000 for 8 months in a business. If the total profit is ₹8,700, find A's share.",
         ["₹4,000", "₹4,300", "₹4,500", "₹4,800"], 2,
         "Capital-time: A = 5000 × 12 = 60,000; B = 7000 × 8 = 56,000. Ratio = 60,000 : 56,000 = 15 : 14. Total parts = 29. A's share = (15/29) × 8700 = ₹4,500. Key Learning Point: Profit is shared in the ratio of (capital × time), not capital alone.", "MEDIUM"),
        # Q4
        ("Simplify the ratio 72:108.",
         ["1:2", "2:3", "3:4", "4:5"], 1,
         "HCF of 72 and 108 = 36. 72 ÷ 36 : 108 ÷ 36 = 2 : 3. Key Learning Point: Divide both terms by their HCF to write the ratio in its simplest form.", "EASY"),
        # Q5
        ("Divide ₹750 between two people in the ratio 2:3.",
         ["₹280 and ₹470", "₹300 and ₹450", "₹320 and ₹430", "₹340 and ₹410"], 1,
         "Total parts = 2 + 3 = 5. First share = (2/5) × 750 = ₹300. Second share = (3/5) × 750 = ₹450. Key Learning Point: Divide the total by the sum of the ratio parts, then multiply by each part.", "EASY"),
        # Q6
        ("The speeds of two trains are in the ratio 5:6. If the slower train covers 150 km in 3 hours, find the speed of the faster train.",
         ["50 km/h", "55 km/h", "60 km/h", "65 km/h"], 2,
         "Speed of slower train = 150/3 = 50 km/h. Speed ratio: faster/slower = 6/5. Speed of faster train = (6/5) × 50 = 60 km/h. Key Learning Point: Find the actual value of one quantity first, then use the ratio to find the other.", "EASY"),
        # Q7
        ("If A:B = 3:4 and B:C = 5:7, find A:B:C.",
         ["15:20:28", "3:4:7", "9:12:21", "6:8:14"], 0,
         "A:B = 3:4 = 15:20 (multiplying by 5). B:C = 5:7 = 20:28 (multiplying by 4). A:B:C = 15:20:28. Key Learning Point: Make the common term (B) equal in both ratios before combining them.", "EASY"),
        # Q8
        ("Find the sub-duplicate ratio of 25:64.",
         ["5:8", "25:8", "5:64", "10:16"], 0,
         "Sub-duplicate ratio of a:b = √a : √b = √25 : √64 = 5 : 8. Key Learning Point: Sub-duplicate ratio means taking the square root of each term; duplicate ratio means squaring each term.", "EASY"),
        # Q9
        ("A sum of money is divided among A, B and C in the ratio 1:2:3. If C receives ₹180 more than A, find the total sum.",
         ["₹450", "₹480", "₹540", "₹600"], 2,
         "Let the shares be x, 2x and 3x. C − A = 3x − x = 2x = ₹180 ⟹ x = ₹90. Total sum = x + 2x + 3x = 6x = 6 × 90 = ₹540. Key Learning Point: Use the difference in parts to find the value of one part, then scale to the total.", "EASY"),
        # Q10
        ("A container has 25 litres of pure milk. 5 litres are withdrawn and replaced with water; the same process is repeated once more. Find the quantity of milk left in the container.",
         ["14 litres", "15 litres", "16 litres", "17 litres"], 2,
         "Fraction removed each time = 5/25 = 1/5; fraction remaining = 4/5. After two operations, milk left = 25 × (4/5) × (4/5) = 25 × 16/25 = 16 litres. Key Learning Point: Milk left after n replacements = Initial quantity × (1 − removed/total)ⁿ.", "MEDIUM"),
        # Q11
        ("Find the fourth proportional to 3, 5, and 18.",
         ["26", "28", "30", "32"], 2,
         "3 : 5 :: 18 : x. 3x = 5 × 18 ⟹ x = 90/3 = 30. Key Learning Point: For the fourth proportional to a, b, c: x = (b × c)/a.", "EASY"),
        # Q12
        ("A mixture of 35 litres contains milk and water in the ratio 5:2. How much water must be added to make the ratio of milk to water 5:3?",
         ["3 litres", "4 litres", "5 litres", "6 litres"], 2,
         "Milk = (5/7) × 35 = 25 litres; Water = (2/7) × 35 = 10 litres. For milk : water = 5 : 3, water required = 25 × (3/5) = 15 litres. Water to be added = 15 − 10 = 5 litres. Key Learning Point: When water is added, the quantity of milk stays the same; use it to find the required water.", "MEDIUM"),
        # Q13
        ("Two numbers are in the ratio 7:8. If their product is 504, find the larger number.",
         ["21", "24", "27", "30"], 1,
         "Let the numbers be 7x and 8x. 7x × 8x = 504 ⟹ 56x² = 504 ⟹ x² = 9 ⟹ x = 3. Larger number = 8x = 8 × 3 = 24. Key Learning Point: Represent the numbers as multiples of x and use the product condition to find x.", "MEDIUM"),
        # Q14
        ("A bag contains 25 paise, 50 paise, and ₹1 coins in the ratio 4:5:6. If the total value of the coins is ₹380, find the number of ₹1 coins.",
         ["220", "230", "240", "250"], 2,
         "Let the number of coins be 4x, 5x and 6x. Value = 4x(0.25) + 5x(0.50) + 6x(1) = x + 2.5x + 6x = 9.5x. 9.5x = 380 ⟹ x = 40. Number of ₹1 coins = 6x = 240. Key Learning Point: Convert the count of each coin type into its rupee value before adding.", "MEDIUM"),
        # Q15
        ("On a map with a scale of 1:2,50,000, the area of a lake is shown as 4 sq. cm. Find the actual area of the lake in sq. km. (1 km = 1,00,000 cm)",
         ["20 sq. km", "22 sq. km", "25 sq. km", "28 sq. km"], 2,
         "1 cm on the map = 2,50,000 cm = 2.5 km. 1 sq. cm on the map = (2.5)² = 6.25 sq. km. Actual area = 4 × 6.25 = 25 sq. km. Key Learning Point: For area on a map, square the linear scale (duplicate ratio).", "MEDIUM"),
        # Q16
        ("Two numbers are in the ratio 5:6. If the sum of their squares is 976, find the smaller number.",
         ["16", "18", "20", "22"], 2,
         "Let the numbers be 5x and 6x. (5x)² + (6x)² = 976 ⟹ 25x² + 36x² = 976 ⟹ 61x² = 976 ⟹ x² = 16 ⟹ x = 4. Smaller number = 5x = 5 × 4 = 20. Key Learning Point: Set up the sum-of-squares equation using the ratio multiples, then solve for x.", "MEDIUM"),
        # Q17
        ("A, B and C start a business with capitals of ₹4,000, ₹5,000 and ₹6,000 respectively. A and B invest for 12 months, while C withdraws after 6 months. If the total profit is ₹6,000, find C's share.",
         ["₹1,250", "₹1,500", "₹1,750", "₹2,000"], 1,
         "Capital-time: A = 4000 × 12 = 48,000; B = 5000 × 12 = 60,000; C = 6000 × 6 = 36,000. Ratio = 48,000 : 60,000 : 36,000 = 4 : 5 : 3. Total parts = 12; C's share = (3/12) × 6000 = ₹1,500. Key Learning Point: When a partner withdraws early, use only the months that partner's capital was actually invested.", "MEDIUM"),
        # Q18
        ("Three numbers are in continued proportion. If the first number is 9 and the third is 16, find the sum of all three numbers.",
         ["35", "36", "37", "38"], 2,
         "For continued proportion a : b = b : c, so b² = a × c. b² = 9 × 16 = 144 ⟹ b = 12. Sum = 9 + 12 + 16 = 37. Key Learning Point: In a continued proportion, the middle term is the mean proportional: b = √(a × c).", "MEDIUM"),
        # Q19
        ("If A:B = 4:5 and B:C = 3:4, find A:B:C.",
         ["12:15:20", "4:5:9", "8:10:15", "16:20:25"], 0,
         "A:B = 4:5 = 12:15 (multiplying by 3). B:C = 3:4 = 15:20 (multiplying by 5). A:B:C = 12:15:20. Key Learning Point: Take the LCM of the two values of the common term (5 and 3 → 15) and scale both ratios to it.", "EASY"),
        # Q20
        ("Find the mean proportion between 16 and 36.",
         ["20", "22", "24", "26"], 2,
         "Mean proportion = √(16 × 36) = √576 = 24. Key Learning Point: The mean proportion between a and b is √(a × b).", "EASY"),
        # Q21
        ("A can complete a piece of work in 15 days and B can complete the same work in 10 days. If they work together, in how many days will the work be completed?",
         ["5 days", "6 days", "7 days", "8 days"], 1,
         "A's 1-day work = 1/15; B's 1-day work = 1/10. Combined 1-day work = 1/15 + 1/10 = 2/30 + 3/30 = 5/30 = 1/6. Time taken together = 6 days. Key Learning Point: Add the work rates, then take the reciprocal. Shortcut: (a × b)/(a + b) = (15 × 10)/25 = 6 days.", "EASY"),
        # Q22
        ("The present ages of two sisters are in the ratio 2:3. After 10 years, the ratio of their ages will be 3:4. Find their present ages.",
         ["16 and 24 years", "18 and 27 years", "20 and 30 years", "22 and 33 years"], 2,
         "Let the present ages be 2x and 3x. (2x + 10)/(3x + 10) = 3/4. 4(2x + 10) = 3(3x + 10) ⟹ 8x + 40 = 9x + 30 ⟹ x = 10. Present ages = 2(10) = 20 years and 3(10) = 30 years. Key Learning Point: Add the given number of years to each age and equate to the new ratio.", "MEDIUM"),
        # Q23
        ("If 8 workers working 5 hours a day earn ₹6,000 in total, how much will 12 workers working 6 hours a day earn, at the same rate?",
         ["₹9,800", "₹10,200", "₹10,800", "₹11,200"], 2,
         "Rate per worker-hour = 6000 / (8 × 5) = ₹150. New earnings = 150 × (12 × 6) = ₹10,800. Key Learning Point: In joint variation, find the rate per unit of the combined quantity (worker-hours), then apply it to the new situation.", "MEDIUM"),
        # Q24
        ("The sum of two numbers is 245. If 15 is added to each number, the ratio of the new numbers becomes 5:6. Find the two numbers.",
         ["105 and 140", "110 and 135", "115 and 130", "120 and 125"], 1,
         "a + b = 245. After adding 15 to each: (a + 15) + (b + 15) = 275. Splitting 275 in the ratio 5:6 gives a + 15 = 125, b + 15 = 150. So a = 110 and b = 135. Key Learning Point: When a constant is added to both numbers, adjust the total first, then divide it in the new ratio.", "MEDIUM"),
        # Q25
        ("Two numbers are in the ratio 5:6. If their product is 480, find the smaller number.",
         ["16", "18", "20", "22"], 2,
         "Let the numbers be 5x and 6x. 5x × 6x = 480 ⟹ 30x² = 480 ⟹ x² = 16 ⟹ x = 4. Smaller number = 5x = 5 × 4 = 20. Key Learning Point: Represent the numbers as multiples of x and use the product condition to find x.", "MEDIUM"),
        # Q26
        ("The ratio of the salaries of A and B is 4:3. A's salary increases by 50% and B's salary increases by 25%. Find the new ratio of their salaries.",
         ["6:5", "7:5", "8:5", "9:5"], 2,
         "New salary of A = 4 × (150/100) = 6. New salary of B = 3 × (125/100) = 3.75. New ratio = 6 : 3.75 = 24 : 15 = 8 : 5. Key Learning Point: Multiply each term by its own growth factor, then simplify the new ratio.", "MEDIUM"),
        # Q27
        ("10 men or 15 women can complete a piece of work in the same number of days. Find the ratio of the efficiency of one man to one woman.",
         ["2:3", "3:2", "5:3", "3:5"], 1,
         "10 × (man's efficiency) = 15 × (woman's efficiency). Man's efficiency : Woman's efficiency = 15 : 10 = 3 : 2. Key Learning Point: Efficiency is inversely proportional to the number of workers needed for the same work in the same time.", "EASY"),
        # Q28
        ("Two numbers are in the ratio 11:13. If their HCF is 6, find their LCM.",
         ["792", "825", "858", "891"], 2,
         "Since 11 and 13 are co-prime, the numbers are 11 × 6 = 66 and 13 × 6 = 78. LCM = 11 × 13 × 6 = 858. Key Learning Point: For two numbers in a co-prime ratio a:b, LCM = a × b × HCF.", "MEDIUM"),
        # Q29
        ("Two numbers are in the ratio 11:13. If each number is decreased by 6, the ratio becomes 5:6. Find the numbers.",
         ["55 and 65", "60 and 71", "66 and 78", "72 and 85"], 2,
         "Let the numbers be 11x and 13x. (11x − 6)/(13x − 6) = 5/6. 6(11x − 6) = 5(13x − 6) ⟹ 66x − 36 = 65x − 30 ⟹ x = 6. Numbers = 11(6) = 66 and 13(6) = 78. Key Learning Point: When the same value is subtracted from both terms, form an equation with the new ratio and solve for x.", "MEDIUM"),
        # Q30
        ("In a survey of 900 people, the number who prefer cricket only, football only, both, and neither are in the ratio 3:2:4:1. Find the number of people who prefer neither.",
         ["70", "80", "90", "100"], 2,
         "Total parts = 3 + 2 + 4 + 1 = 10. Value of 1 part = 900/10 = 90. People who prefer neither = 1 part = 90. Key Learning Point: Find the value of one part from the total before extracting any single category.", "MEDIUM")
    ]

    # 30 Graded Assessment (Tamil)
    graded_ta = [
        # Q1
        ("25 பேனாக்களின் விலை ₹375. அதே விலையில் 60 பேனாக்களின் விலையைக் காண்க.",
         ["₹800", "₹850", "₹900", "₹950"], 2,
         "1 பேனாவின் விலை = 375 ÷ 25 = ₹15. 60 பேனாக்களின் விலை = 15 × 60 = ₹900. முக்கியக் கற்றல் கருத்து: நேர் விகிதசமத்தில், முதலில் ஓர் அலகின் மதிப்பைக் கண்டறிந்து, பின்னர் தேவையான அளவால் பெருக்கவும்.", "EASY"),
        # Q2
        ("இரண்டு எண்கள் 2:3 என்ற விகிதத்தில் உள்ளன. ஒவ்வொன்றுடனும் 6 கூட்டினால், விகிதம் 5:7 ஆகிறது. அவ்வெண்களைக் காண்க.",
         ["18 மற்றும் 27", "20 மற்றும் 30", "24 மற்றும் 36", "28 மற்றும் 42"], 2,
         "எண்கள் 2x மற்றும் 3x என்க. (2x + 6)/(3x + 6) = 5/7. 7(2x + 6) = 5(3x + 6) ⟹ 14x + 42 = 15x + 30 ⟹ x = 12. எண்கள் = 2(12) = 24 மற்றும் 3(12) = 36. முக்கியக் கற்றல் கருத்து: இரண்டு உறுப்புகளுடனும் ஒரே மதிப்பு கூட்டப்படும்போது, புதிய விகிதத்துடன் ஒரு சமன்பாட்டை அமைத்துப் பெருக்கியைக் காணவும்.", "MEDIUM"),
        # Q3
        ("ஒரு வியாபாரத்தில் A ₹5,000-ஐ 12 மாதங்களுக்கும், B ₹7,000-ஐ 8 மாதங்களுக்கும் முதலீடு செய்கின்றனர். மொத்த இலாபம் ₹8,700 எனில், A-இன் பங்கைக் காண்க.",
         ["₹4,000", "₹4,300", "₹4,500", "₹4,800"], 2,
         "முதலீடு × காலம்: A = 5000 × 12 = 60,000; B = 7000 × 8 = 56,000. விகிதம் = 60,000 : 56,000 = 15 : 14. மொத்தப் பகுதிகள் = 29. A-இன் பங்கு = (15/29) × 8700 = ₹4,500. முக்கியக் கற்றல் கருத்து: இலாபம் முதலீட்டின் விகிதத்தில் மட்டும் அல்லாமல், (முதலீடு × காலம்) விகிதத்தில் பகிரப்படுகிறது.", "MEDIUM"),
        # Q4
        ("72:108 என்ற விகிதத்தைச் சுருக்குக.",
         ["1:2", "2:3", "3:4", "4:5"], 1,
         "72 மற்றும் 108-இன் மீ.பொ.வ = 36. 72 ÷ 36 : 108 ÷ 36 = 2 : 3. முக்கியக் கற்றல் கருத்து: விகிதத்தை எளிய வடிவில் எழுத, இரண்டு உறுப்புகளையும் அவற்றின் மீ.பொ.வ-ஆல் வகுக்கவும்.", "EASY"),
        # Q5
        ("₹750-ஐ இருவருக்கு 2:3 என்ற விகிதத்தில் பிரிக்கவும்.",
         ["₹280 மற்றும் ₹470", "₹300 மற்றும் ₹450", "₹320 மற்றும் ₹430", "₹340 மற்றும் ₹410"], 1,
         "மொத்தப் பகுதிகள் = 2 + 3 = 5. முதல் பங்கு = (2/5) × 750 = ₹300. இரண்டாம் பங்கு = (3/5) × 750 = ₹450. முக்கியக் கற்றல் கருத்து: மொத்தத்தை விகிதப் பகுதிகளின் கூடுதலால் வகுத்து, பின்னர் ஒவ்வொரு பகுதியாலும் பெருக்கவும்.", "EASY"),
        # Q6
        ("இரண்டு தொடர்வண்டிகளின் வேக விகிதம் 5:6. மெதுவான தொடர்வண்டி 150 கி.மீ தூரத்தை 3 மணி நேரத்தில் கடந்தால், வேகமான தொடர்வண்டியின் வேகத்தைக் காண்க.",
         ["50 கி.மீ/மணி", "55 கி.மீ/மணி", "60 கி.மீ/மணி", "65 கி.மீ/மணி"], 2,
         "மெதுவான தொடர்வண்டியின் வேகம் = 150/3 = 50 கி.மீ/மணி. வேக விகிதம்: வேகமானது/மெதுவானது = 6/5. வேகமான தொடர்வண்டியின் வேகம் = (6/5) × 50 = 60 கி.மீ/மணி. முக்கியக் கற்றல் கருத்து: முதலில் ஓர் அளவின் உண்மையான மதிப்பைக் கண்டறிந்து, பின்னர் விகிதத்தைப் பயன்படுத்தி மற்றொன்றைக் காணவும்.", "EASY"),
        # Q7
        ("A:B = 3:4 மற்றும் B:C = 5:7 எனில், A:B:C-ஐக் காண்க.",
         ["15:20:28", "3:4:7", "9:12:21", "6:8:14"], 0,
         "A:B = 3:4 = 15:20 (5-ஆல் பெருக்க). B:C = 5:7 = 20:28 (4-ஆல் பெருக்க). A:B:C = 15:20:28. முக்கியக் கற்றல் கருத்து: இணைக்கும் முன் இரண்டு விகிதங்களிலும் பொது உறுப்பை (B) சமமாக்கவும்.", "EASY"),
        # Q8
        ("25:64-இன் வர்க்கமூல விகிதத்தைக் காண்க.",
         ["5:8", "25:8", "5:64", "10:16"], 0,
         "a:b-இன் வர்க்கமூல விகிதம் = √a : √b = √25 : √64 = 5 : 8. முக்கியக் கற்றல் கருத்து: வர்க்கமூல விகிதம் என்பது ஒவ்வோர் உறுப்பின் வர்க்கமூலத்தை எடுப்பதாகும்; இருமடி விகிதம் என்பது ஒவ்வோர் உறுப்பையும் வர்க்கப்படுத்துவதாகும்.", "EASY"),
        # Q9
        ("ஒரு தொகை A, B, C ஆகியோருக்கு 1:2:3 என்ற விகிதத்தில் பிரிக்கப்படுகிறது. A-ஐ விட C ₹180 அதிகம் பெற்றால், மொத்தத் தொகையைக் காண்க.",
         ["₹450", "₹480", "₹540", "₹600"], 2,
         "பங்குகள் x, 2x, 3x என்க. C − A = 3x − x = 2x = ₹180 ⟹ x = ₹90. மொத்தத் தொகை = x + 2x + 3x = 6x = 6 × 90 = ₹540. முக்கியக் கற்றல் கருத்து: பகுதிகளின் வேறுபாட்டைக் கொண்டு ஒரு பகுதியின் மதிப்பைக் கண்டறிந்து, பின்னர் மொத்தத்திற்கு மாற்றியமைக்கவும்.", "EASY"),
        # Q10
        ("ஒரு கொள்கலனில் 25 லிட்டர் தூய பால் உள்ளது. 5 லிட்டர் எடுக்கப்பட்டுத் தண்ணீரால் நிரப்பப்படுகிறது; இதே செயல்முறை மேலும் ஒருமுறை செய்யப்படுகிறது. கொள்கலனில் மீதமுள்ள பாலின் அளவைக் காண்க.",
         ["14 லிட்டர்", "15 லிட்டர்", "16 லிட்டர்", "17 லிட்டர்"], 2,
         "ஒவ்வொரு முறையும் எடுக்கப்படும் பின்னம் = 5/25 = 1/5; மீதமுள்ள பின்னம் = 4/5. இரண்டு செயல்களுக்குப் பின், மீதமுள்ள பால் = 25 × (4/5) × (4/5) = 25 × 16/25 = 16 லிட்டர். முக்கியக் கற்றல் கருத்து: n முறை மாற்றீட்டுக்குப்பின் மீதமுள்ள பால் = தொடக்க அளவு × (1 − எடுக்கப்பட்டது/மொத்தம்)ⁿ.", "MEDIUM"),
        # Q11
        ("3, 5, 18 ஆகியவற்றின் நான்காம் விகிதசம உறுப்பைக் காண்க.",
         ["26", "28", "30", "32"], 2,
         "3 : 5 :: 18 : x. 3x = 5 × 18 ⟹ x = 90/3 = 30. முக்கியக் கற்றல் கருத்து: a, b, c-இன் நான்காம் விகிதசம உறுப்பு: x = (b × c)/a.", "EASY"),
        # Q12
        ("35 லிட்டர் கலவையில் பாலும் தண்ணீரும் 5:2 என்ற விகிதத்தில் உள்ளன. பால் : தண்ணீர் விகிதத்தை 5:3 ஆக்க எவ்வளவு தண்ணீர் சேர்க்க வேண்டும்?",
         ["3 லிட்டர்", "4 லிட்டர்", "5 லிட்டர்", "6 லிட்டர்"], 2,
         "பால் = (5/7) × 35 = 25 லிட்டர்; தண்ணீர் = (2/7) × 35 = 10 லிட்டர். பால்: தண்ணீர் = 5 : 3 ஆக, தேவையான தண்ணீர் = 25 × (3/5) = 15 லிட்டர். சேர்க்க வேண்டிய தண்ணீர் = 15 − 10 = 5 லிட்டர். முக்கியக் கற்றல் கருத்து: தண்ணீர் சேர்க்கப்படும்போது பாலின் அளவு மாறாது; தேவையான தண்ணீரைக்காண அதைப் பயன்படுத்தவும்.", "MEDIUM"),
        # Q13
        ("இரண்டு எண்கள் 7:8 என்ற விகிதத்தில் உள்ளன. அவற்றின் பெருக்கற்பலன் 504 எனில், பெரிய எண்ணைக் காண்க.",
         ["21", "24", "27", "30"], 1,
         "எண்கள் 7x மற்றும் 8x என்க. 7x × 8x = 504 ⟹ 56x² = 504 ⟹ x² = 9 ⟹ x = 3. பெரிய எண் = 8x = 8 × 3 = 24. முக்கியக் கற்றல் கருத்து: எண்களை x-இன் மடங்குகளாக எழுதிப் பெருக்கற்பலன் நிபந்தனையைக் கொண்டு x-ஐக் காணவும்.", "MEDIUM"),
        # Q14
        ("ஒரு பையில் 25 பைசா, 50 பைசா, ₹1 நாணயங்கள் 4:5:6 என்ற விகிதத்தில் உள்ளன. நாணயங்களின் மொத்த மதிப்பு ₹380 எனில், ₹1 நாணயங்களின் எண்ணிக்கையைக் காண்க.",
         ["220", "230", "240", "250"], 2,
         "நாணயங்களின் எண்ணிக்கை 4x, 5x, 6x என்க. மதிப்பு = 4x(0.25) + 5x(0.50) + 6x(1) = x + 2.5x + 6x = 9.5x. 9.5x = 380 ⟹ x = 40. ₹1 நாணயங்களின் எண்ணிக்கை = 6x = 240. முக்கியக் கற்றல் கருத்து: கூட்டும் முன் ஒவ்வொரு வகை நாணயத்தின் எண்ணிக்கையையும் அதன் ரூபாய் மதிப்பாக மாற்றவும்.", "MEDIUM"),
        # Q15
        ("1:2,50,000 அளவுகோல் கொண்ட ஒரு வரைபடத்தில், ஓர் ஏரியின் பரப்பு 4 ச.செ.மீ ஆகக் காட்டப்பட்டுள்ளது. அவ்வேரியின் உண்மையான பரப்பை ச.கி.மீ-இல் காண்க. (1 கி.மீ = 1,00,000 செ.மீ)",
         ["20 ச.கி.மீ", "22 ச.கி.மீ", "25 ச.கி.மீ", "28 ச.கி.மீ"], 2,
         "வரைபடத்தில் 1 செ.மீ = 2,50,000 செ.மீ = 2.5 கி.மீ. வரைபடத்தில் 1 ச.செ.மீ = (2.5)² = 6.25 ச.கி.மீ. உண்மையான பரப்பு = 4 × 6.25 = 25 ச.கி.மீ. முக்கியக் கற்றல் கருத்து: வரைபடப் பரப்புக்கு, நேரியல் அளவுகோலை வர்க்கப்படுத்தவும் (இருமடி விகிதம்).", "MEDIUM"),
        # Q16
        ("இரண்டு எண்கள் 5:6 என்ற விகிதத்தில் உள்ளன. அவற்றின் வர்க்கங்களின் கூடுதல் 976 எனில், சிறிய எண்ணைக் காண்க.",
         ["16", "18", "20", "22"], 2,
         "எண்கள் 5x மற்றும் 6x என்க. (5x)² + (6x)² = 976 ⟹ 25x² + 36x² = 976 ⟹ 61x² = 976 ⟹ x² = 16 ⟹ x = 4. சிறிய எண் = 5x = 5 × 4 = 20. முக்கியக் கற்றல் கருத்து: விகித மடங்குகளைக் கொண்டு வர்க்கக் கூடுதல் சமன்பாட்டை அமைத்து x-ஐக் காணவும்.", "MEDIUM"),
        # Q17
        ("A, B, C ஆகியோர் முறையே ₹4,000, ₹5,000, ₹6,000 முதலீட்டுடன் ஒரு வியாபாரத்தைத் தொடங்குகின்றனர். A மற்றும் B 12 மாதங்களுக்கு முதலீடு செய்கின்றனர்; C 6 மாதங்களுக்குப் பின் விலகுகிறார். மொத்த இலாபம் ₹6,000 எனில், C-இன் பங்கைக் காண்க.",
         ["₹1,250", "₹1,500", "₹1,750", "₹2,000"], 1,
         "முதலீடு × காலம்: A = 4000 × 12 = 48,000; B = 5000 × 12 = 60,000; C = 6000 × 6 = 36,000. விகிதம் = 48,000 : 60,000 : 36,000 = 4 : 5 : 3. மொத்தப் பகுதிகள் = 12; C-இன் பங்கு = (3/12) × 6000 = ₹1,500. முக்கியக் கற்றல் கருத்து: ஒரு கூட்டாளி முன்னதாக விலகும்போது, அவரது முதலீடு உண்மையில் இருந்த மாதங்களை மட்டுமே பயன்படுத்தவும்.", "MEDIUM"),
        # Q18
        ("மூன்று எண்கள் தொடர் விகிதசமத்தில் உள்ளன. முதல் எண் 9, மூன்றாம் எண் 16 எனில், மூன்று எண்களின் கூடுதலைக் காண்க.",
         ["35", "36", "37", "38"], 2,
         "தொடர் விகிதசமத்தில் a : b = b : c, எனவே b² = a × c. b² = 9 × 16 = 144 ⟹ b = 12. கூடுதல் = 9 + 12 + 16 = 37. முக்கியக் கற்றல் கருத்து: தொடர் விகிதசமத்தில், நடு உறுப்பு இடை விகிதசம உறுப்பாகும்: b = √(a × c).", "MEDIUM"),
        # Q19
        ("A:B = 4:5 மற்றும் B:C = 3:4 எனில், A:B:C-ஐக் காண்க.",
         ["12:15:20", "4:5:9", "8:10:15", "16:20:25"], 0,
         "A:B = 4:5 = 12:15 (3-ஆல் பெருக்க). B:C = 3:4 = 15:20 (5-ஆல் பெருக்க). A:B:C = 12:15:20. முக்கியக் கற்றல் கருத்து: பொது உறுப்பின் இரண்டு மதிப்புகளின் மீ.பொ.ம-வை (5 மற்றும் 3 → 15) எடுத்து, இரண்டு விகிதங்களையும் அதற்கு மாற்றியமைக்கவும்.", "EASY"),
        # Q20
        ("16 மற்றும் 36-இன் இடை விகிதசம உறுப்பைக் காண்க.",
         ["20", "22", "24", "26"], 2,
         "இடை விகிதசம உறுப்பு = √(16 × 36) = √576 = 24. முக்கியக் கற்றல் கருத்து: a மற்றும் b-இன் இடை விகிதசம உறுப்பு √(a × b) ஆகும்.", "EASY"),
        # Q21
        ("A ஒரு வேலையை 15 நாட்களிலும், B அதே வேலையை 10 நாட்களிலும் முடிக்க முடியும். இருவரும் சேர்ந்து வேலை செய்தால், அவ்வேலை எத்தனை நாட்களில் முடியும்?",
         ["5 நாட்கள்", "6 நாட்கள்", "7 நாட்கள்", "8 நாட்கள்"], 1,
         "A-இன் 1 நாள் வேலை = 1/15; B-இன் 1 நாள் வேலை = 1/10. ஒருங்கிணைந்த 1 நாள் வேலை = 1/15 + 1/10 = 2/30 + 3/30 = 5/30 = 1/6. இருவரும் சேர்ந்து எடுக்கும் காலம் = 6 நாட்கள். முக்கியக் கற்றல் கருத்து: வேலை வீதங்களைக் கூட்டித் தலைகீழியை எடுக்கவும். குறுக்கு வழி: (a × b)/(a + b) = (15 × 10)/25 = 6 நாட்கள்.", "EASY"),
        # Q22
        ("இரண்டு சகோதரிகளின் தற்போதைய வயதுகள் 2:3 என்ற விகிதத்தில் உள்ளன. 10 ஆண்டுகளுக்குப் பின் அவர்களின் வயது விகிதம் 3:4 ஆக இருக்கும். அவர்களின் தற்போதைய வயதுகளைக் காண்க.",
         ["16 மற்றும் 24 ஆண்டுகள்", "18 மற்றும் 27 ஆண்டுகள்", "20 மற்றும் 30 ஆண்டுகள்", "22 மற்றும் 33 ஆண்டுகள்"], 2,
         "தற்போதைய வயதுகள் 2x மற்றும் 3x என்க. (2x + 10)/(3x + 10) = 3/4. 4(2x + 10) = 3(3x + 10) ⟹ 8x + 40 = 9x + 30 ⟹ x = 10. தற்போதைய வயதுகள் = 2(10) = 20 ஆண்டுகள் மற்றும் 3(10) = 30 ஆண்டுகள். முக்கியக் கற்றல் கருத்து: கொடுக்கப்பட்ட ஆண்டுகளை ஒவ்வொரு வயதுடனும் கூட்டிப் புதிய விகிதத்துடன் சமப்படுத்தவும்.", "MEDIUM"),
        # Q23
        ("நாளொன்றுக்கு 5 மணி நேரம் வேலை செய்யும் 8 பணியாளர்கள் மொத்தம் ₹6,000 ஈட்டினால், அதே வீதத்தில் நாளொன்றுக்கு 6 மணி நேரம் வேலை செய்யும் 12 பணியாளர்கள் எவ்வளவு ஈட்டுவர்?",
         ["₹9,800", "₹10,200", "₹10,800", "₹11,200"], 2,
         "ஒரு பணியாளர்-மணிக்கான வீதம் = 6000 / (8 × 5) = ₹150. புதிய வருவாய் = 150 × (12 × 6) = ₹10,800. முக்கியக் கற்றல் கருத்து: கூட்டு மாறுபாட்டில், ஒருங்கிணைந்த அளவின் (பணியாளர்-மணி) ஓர் அலகுக்கான வீதத்தைக் கண்டறிந்து, புதிய சூழலுக்குப் பயன்படுத்தவும்.", "MEDIUM"),
        # Q24
        ("இரண்டு எண்களின் கூடுதல் 245. ஒவ்வோர் எண்ணுடனும் 15 கூட்டினால், புதிய எண்களின் விகிதம் 5:6 ஆகிறது. அவ்விரண்டு எண்களைக் காண்க.",
         ["105 மற்றும் 140", "110 மற்றும் 135", "115 மற்றும் 130", "120 மற்றும் 125"], 1,
         "a + b = 245. ஒவ்வொன்றுடனும் 15 கூட்டிய பின்: (a + 15) + (b + 15) = 275. 275-ஐ 5:6 என்ற விகிதத்தில் பிரிக்க: a + 15 = 125, b + 15 = 150. எனவே a = 110 மற்றும் b = 135. முக்கியக் கற்றல் கருத்து: இரண்டு எண்களுடனும் ஒரு மாறிலி கூட்டப்படும்போது, முதலில் மொத்தத்தைச் சரிசெய்து, பின்னர் அதைப் புதிய விகிதத்தில் பிரிக்கவும்.", "MEDIUM"),
        # Q25
        ("இரண்டு எண்கள் 5:6 என்ற விகிதத்தில் உள்ளன. அவற்றின் பெருக்கற்பலன் 480 எனில், சிறிய எண்ணைக் காண்க.",
         ["16", "18", "20", "22"], 2,
         "எண்கள் 5x மற்றும் 6x என்க. 5x × 6x = 480 ⟹ 30x² = 480 ⟹ x² = 16 ⟹ x = 4. சிறிய எண் = 5x = 5 × 4 = 20. முக்கியக் கற்றல் கருத்து: எண்களை x-இன் மடங்குகளாக எழுதிப் பெருக்கற்பலன் நிபந்தனையைக் கொண்டு x-ஐக் காணவும்.", "MEDIUM"),
        # Q26
        ("A மற்றும் B-இன் சம்பள விகிதம் 4:3. A-இன் சம்பளம் 50%, B-இன் சம்பளம் 25% அதிகரிக்கிறது. அவர்களின் சம்பளத்தின் புதிய விகிதத்தைக் காண்க.",
         ["6:5", "7:5", "8:5", "9:5"], 2,
         "A-இன் புதிய சம்பளம் = 4 × (150/100) = 6. B-இன் புதிய சம்பளம் = 3 × (125/100) = 3.75. புதிய விகிதம் = 6 : 3.75 = 24 : 15 = 8 : 5. முக்கியக் கற்றல் கருத்து: ஒவ்வோர் உறுப்பையும் அதன் சொந்த வளர்ச்சிக் காரணியால் பெருக்கி, பின்னர் புதிய விகிதத்தைச் சுருக்கவும்.", "MEDIUM"),
        # Q27
        ("10 ஆண்கள் அல்லது 15 பெண்கள் ஒரு வேலையை ஒரே எண்ணிக்கையிலான நாட்களில் முடிக்க முடியும். ஓர் ஆணுக்கும் ஒரு பெண்ணுக்கும் இடையிலான திறன் விகிதத்தைக் காண்க.",
         ["2:3", "3:2", "5:3", "3:5"], 1,
         "10 × (ஆணின் திறன்) = 15 × (பெண்ணின் திறன்). ஆணின் திறன் : பெண்ணின் திறன் = 15 : 10 = 3 : 2. முக்கியக் கற்றல் கருத்து: ஒரே வேலையை ஒரே காலத்தில் முடிக்கத் தேவைப்படும் பணியாளர்களின் எண்ணிக்கைக்குத் திறன் எதிர்விகிதத்தில் உள்ளது.", "EASY"),
        # Q28
        ("இரண்டு எண்கள் 11:13 என்ற விகிதத்தில் உள்ளன. அவற்றின் மீ.பொ.வ 6 எனில், அவற்றின் மீ.பொ.ம-வைக் காண்க.",
         ["792", "825", "858", "891"], 2,
         "11 மற்றும் 13 சார்பகா எண்கள் என்பதால், எண்கள் 11 × 6 = 66 மற்றும் 13 × 6 = 78. மீ.பொ.ம = 11 × 13 × 6 = 858. முக்கியக் கற்றல் கருத்து: a:b என்ற சார்பகா விகிதத்திலுள்ள இரண்டு எண்களுக்கு, மீ.பொ.ம = a × b × மீ.பொ.வ.", "MEDIUM"),
        # Q29
        ("இரண்டு எண்கள் 11:13 என்ற விகிதத்தில் உள்ளன. ஒவ்வோர் எண்ணிலிருந்தும் 6 கழித்தால், விகிதம் 5:6 ஆகிறது. அவ்வெண்களைக் காண்க.",
         ["55 மற்றும் 65", "60 மற்றும் 71", "66 மற்றும் 78", "72 மற்றும் 85"], 2,
         "எண்கள் 11x மற்றும் 13x என்க. (11x − 6)/(13x − 6) = 5/6. 6(11x − 6) = 5(13x − 6) ⟹ 66x − 36 = 65x − 30 ⟹ x = 6. எண்கள் = 11(6) = 66 மற்றும் 13(6) = 78. முக்கியக் கற்றல் கருத்து: இரண்டு உறுப்புகளிலிருந்தும் ஒரே மதிப்பு கழிக்கப்படும்போது, புதிய விகிதத்துடன் ஒரு சமன்பாட்டை அமைத்து x-ஐக் காணவும்.", "MEDIUM"),
        # Q30
        ("900 பேரிடம் நடத்தப்பட்ட ஒரு கணக்கெடுப்பில், கிரிக்கெட் மட்டும், கால்பந்து மட்டும், இரண்டும், எதுவுமில்லை என விரும்புவோரின் எண்ணிக்கை 3:2:4:1 என்ற விகிதத்தில் உள்ளது. எதையும் விரும்பாதோரின் எண்ணிக்கையைக் காண்க.",
         ["70", "80", "90", "100"], 2,
         "மொத்தப் பகுதிகள் = 3 + 2 + 4 + 1 = 10. 1 பகுதியின் மதிப்பு = 900/10 = 90. எதையும் விரும்பாதோர் = 1 பகுதி = 90. முக்கியக் கற்றல் கருத்து: எந்த ஒரு வகையையும் பிரித்தெடுக்கும் முன், மொத்தத்திலிருந்து ஒரு பகுதியின் மதிப்பைக் கண்டறியவும்.", "MEDIUM")
    ]

    out_lines = [
        "/* ============================================================================",
        "   ExamPro LMS - Ratio and Proportion Course Seed Script (Unified Bilingual Model)",
        "   - 1 Course: Ratio and Proportion / விகிதம் மற்றும் விகிதசமம்",
        "   - 2 Assessments (Single unified assessment for both English & Tamil):",
        "       1. Ratio and Proportion - Practice Set (ratio-and-proportion-practice) [55 Questions]",
        "          (25 Worked Examples + 30 Independent Practice in both English & Tamil)",
        "       2. Ratio and Proportion - Graded Assessment (ratio-and-proportion-graded) [30 Questions]",
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
        "-- Clean previous Ratio and Proportion courses and assessments if present",
        "DELETE FROM dbo.Assessments WHERE Slug IN (",
        "    N'ratio-and-proportion-practice', N'ratio-and-proportion-graded',",
        "    N'ratio-practice', N'ratio-graded',",
        "    N'ratio-and-proportion-practice-en', N'ratio-and-proportion-graded-en',",
        "    N'ratio-and-proportion-practice-ta', N'ratio-and-proportion-graded-ta'",
        ");",
        "DELETE FROM dbo.Courses WHERE Slug IN (N'ratio-and-proportion', N'ratio-proportion');",
        "",
        "INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)",
        "VALUES (",
        "    N'Ratio and Proportion / விகிதம் மற்றும் விகிதசமம்',",
        "    N'ratio-and-proportion',",
        "    N'Comprehensive arithmetic module on Ratio and Proportion for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',",
        "    2",
        ");",
        "",
        "DECLARE @CourseId INT = SCOPE_IDENTITY();",
        "",
        "-- Insert ONLY 2 Assessments: 1 Practice and 1 Graded",
        "INSERT INTO dbo.Assessments (",
        "    CourseId, Title, TitleTa, Slug, Description, DescriptionTa, Topic, Difficulty,",
        "    DefaultDurationMinutes, MinDurationMinutes, TotalQuestions, PassPercentage,",
        "    AttemptType, SequentialUnlock, LockdownEnabled, ProctoringEnabled, OrderIndex",
        ")",
        "VALUES",
        "    (@CourseId, N'Ratio and Proportion - Practice Set', N'விகிதம் மற்றும் விகிதசமம் - பயிற்சித் தொகுப்பு', N'ratio-and-proportion-practice',",
        "     N'55 practice questions (Worked Examples + Independent Practice) with instant feedback & step-by-step solutions.',",
        "     N'55 பயிற்சிக் கணக்குகள் (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனடித் தீர்வுகளுடன்.',",
        "     N'Ratio and Proportion', N'EASY', 60, 10, 55, 0, N'PRACTICE', 0, 0, 0, 1),",
        "    (@CourseId, N'Ratio and Proportion - Graded Assessment', N'விகிதம் மற்றும் விகிதசமம் - மதிப்பீட்டுத் தேர்வு', N'ratio-and-proportion-graded',",
        "     N'Official proctored & timed assessment on Ratio and Proportion (30 Questions). Pass with 60% to master this topic.',",
        "     N'விகிதம் மற்றும் விகிதசமத்திற்கான அதிகாரப்பூர்வக் கண்காணிப்புடன் கூடிய தேர்வு (30 வினாக்கள்). தேர்ச்சி 60%.',",
        "     N'Ratio and Proportion', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 2);",
        "",
        "DECLARE @pracId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'ratio-and-proportion-practice');",
        "DECLARE @gradId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'ratio-and-proportion-graded');",
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
                f"N'Ratio and Proportion', {escape_sql(diff)}, {idx + 1})"
            )
            val_rows.append(row)
        out_lines.append(",\n".join(val_rows) + ";\n")

    # 1. Practice Set (55 Questions: 25 worked + 30 indep)
    insert_bilingual_questions("@pracId", worked_en + indep_en, worked_ta + indep_ta)

    # 2. Graded Assessment (30 Questions)
    insert_bilingual_questions("@gradId", graded_en, graded_ta)

    out_lines.append("COMMIT;")
    out_lines.append("PRINT 'Ratio and Proportion Course seeded successfully: 1 Practice Assessment (55 Qs) and 1 Graded Assessment (30 Qs), fully bilingual (English & Tamil).';")
    out_lines.append("GO\n")

    output_path = r"c:\Users\Lenovo\Downloads\LMS\exampro-lms\database\05_ratio_bilingual_seed.sql"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Successfully generated {output_path} with {len(worked_en) + len(indep_en)} practice and {len(graded_en)} graded questions.")

if __name__ == "__main__":
    main()
