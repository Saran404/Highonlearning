# -*- coding: utf-8 -*-
"""Generates 09_number_series_bilingual_seed.sql containing all 85 questions from English and Tamil Number Series PDFs."""
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
        ("Find the next term: 2, 4, 6, 8, ?",
         ["9", "10", "11", "12"], 1,
         "Constant difference of +2. 8+2 = 10. Key Learning Point: Always check for a constant difference (arithmetic series) first, as it is the simplest pattern.", "EASY"),
        # Q2
        ("Find the next term: 5, 10, 15, 20, ?",
         ["22", "24", "25", "30"], 2,
         "Constant difference of +5. 20+5 = 25. Key Learning Point: In an arithmetic series, the difference between every pair of consecutive terms is the same.", "EASY"),
        # Q3
        ("Find the next term: 3, 6, 12, 24, ?",
         ["36", "42", "48", "50"], 2,
         "Constant ratio of ×2. 24×2 = 48. Key Learning Point: If the difference is not constant, check whether the ratio between consecutive terms is constant instead (geometric series).", "EASY"),
        # Q4
        ("Find the next term: 100, 90, 80, 70, ?",
         ["55", "60", "65", "68"], 1,
         "Constant difference of −10. 70−10 = 60. Key Learning Point: Decreasing arithmetic series follow the same logic as increasing ones, with a negative constant difference.", "EASY"),
        # Q5
        ("Find the next term: 1, 4, 9, 16, ?",
         ["20", "22", "24", "25"], 3,
         "These are perfect squares: 1², 2², 3², 4², 5² = 25. Key Learning Point: Recognise perfect square series by checking whether each term is a whole number squared.", "EASY"),
        # Q6
        ("Find the next term: 2, 6, 12, 20, 30, ?",
         ["40", "41", "42", "44"], 2,
         "Differences: 4, 6, 8, 10, 12 (increasing by 2 each time). 30+12 = 42. Pattern: n(n+1) for n=1,2,3… → 1×2, 2×3, 3×4, 4×5, 5×6, 6×7=42. Key Learning Point: When the difference itself increases by a constant amount, write out the differences as a separate row to reveal the pattern.", "EASY"),
        # Q7
        ("Find the next term: 7, 14, 28, 56, ?",
         ["100", "108", "110", "112"], 3,
         "Constant ratio ×2. 56×2 = 112. Key Learning Point: Verify a suspected ratio against every consecutive pair before finalising it as the pattern.", "EASY"),
        # Q8
        ("Find the next term: 3, 8, 15, 24, 35, ?",
         ["46", "47", "48", "50"], 2,
         "Differences: 5, 7, 9, 11, 13 (increasing by 2). 35+13 = 48. Key Learning Point: An increasing-odd-number difference pattern often corresponds to a product or square-based formula (here, n×(n+2)).", "EASY"),
        # Q9
        ("Find the wrong number in the series: 2, 5, 10, 17, 26, 38, 50",
         ["10", "17", "38", "50"], 2,
         "Pattern: n²+1 for n=1..7 → 2, 5, 10, 17, 26, 37, 50. The term 38 breaks the pattern (should be 37). Key Learning Point: Compute the expected value for every position using the suspected formula, then compare against the given series term by term.", "MEDIUM"),
        # Q10
        ("Find the next term: 1, 1, 2, 3, 5, 8, ?",
         ["11", "12", "13", "14"], 2,
         "Fibonacci pattern: each term is the sum of the two preceding terms. 5+8 = 13. Key Learning Point: In a Fibonacci-type series, check whether each term equals the sum of the two terms before it.", "EASY"),
        # Q11
        ("Find the next term: 2, 3, 5, 7, 11, ?",
         ["12", "13", "14", "15"], 1,
         "These are prime numbers in order. The next prime after 11 is 13. Key Learning Point: If no arithmetic or geometric pattern fits, check whether the series consists of prime numbers.", "EASY"),
        # Q12
        ("Find the next term: 4, 9, 16, 25, 36, ?",
         ["42", "45", "47", "49"], 3,
         "Perfect squares starting from 2²: 2², 3², 4², 5², 6², 7² = 49. Key Learning Point: A square series does not always start from 1² – check the starting point carefully.", "EASY"),
        # Q13
        ("Find the next term: 1, 8, 27, 64, ?",
         ["100", "110", "121", "125"], 3,
         "Perfect cubes: 1³, 2³, 3³, 4³, 5³ = 125. Key Learning Point: If squares don’t fit, check whether the series consists of perfect cubes.", "EASY"),
        # Q14
        ("Find the next term: 5, 10, 9, 18, 17, 34, ?",
         ["32", "33", "35", "68"], 1,
         "Alternating operations: ×2, −1, repeating. 5×2=10, 10−1=9, 9×2=18, 18−1=17, 17×2=34, 34−1=33. Key Learning Point: When a single operation doesn’t fit, check whether two operations alternate in a repeating pair.", "MEDIUM"),
        # Q15
        ("Find the missing term: 3, 10, 7, 12, 11, 14, 15, ?",
         ["15", "16", "17", "18"], 1,
         "Odd positions (1st,3rd,5th,7th): 3, 7, 11, 15 (+4 each). Even positions (2nd,4th,6th,8th): 10, 12, 14, ? (+2 each) → 16. Key Learning Point: Split a two-interleaved series into its odd-position and even-position sub-series before looking for a pattern.", "MEDIUM"),
        # Q16
        ("Find the wrong number in the series: 6, 12, 24, 50, 96, 192",
         ["12", "24", "50", "96"], 2,
         "Pattern: ×2 throughout → 6, 12, 24, 48, 96, 192. The term 50 breaks the pattern (should be 48). Key Learning Point: Once a ratio pattern is confirmed with the first few terms, compute the full expected series to spot the mismatch.", "MEDIUM"),
        # Q17
        ("Find the next term: 8, 12, 9, 13, 10, 14, ?",
         ["10", "11", "15", "18"], 1,
         "Alternating operations: +4, −3, repeating. 14−3 = 11. Key Learning Point: In alternating series, identify both operations in the repeating pair before predicting the next term.", "EASY"),
        # Q18
        ("Find the next term: 2, 6, 18, 54, ?",
         ["108", "144", "162", "180"], 2,
         "Constant ratio ×3. 54×3 = 162. Key Learning Point: If ×2 doesn’t fit a geometric series, test other constant ratios such as ×3.", "EASY"),
        # Q19
        ("Find the next term: 100, 50, 25, 12.5, ?",
         ["5", "6", "6.25", "6.5"], 2,
         "Constant ratio ÷2. 12.5÷2 = 6.25. Key Learning Point: Geometric series can involve fractional or decimal ratios, not just whole-number ones.", "EASY"),
        # Q20
        ("Find the next term: 1, 4, 10, 22, 46, ?",
         ["90", "92", "94", "96"], 2,
         "Pattern: each term = 2×(previous term)+2. 46×2+2 = 94. Key Learning Point: When neither a constant difference nor a constant ratio fits alone, test a combined operation such as “×2, then add a constant.”", "MEDIUM"),
        # Q21
        ("Find the wrong number in the series: 5, 10, 17, 26, 37, 50, 64",
         ["17", "26", "50", "64"], 3,
         "Pattern: n²+1 for n=2..8 → 5, 10, 17, 26, 37, 50, 65. The term 64 breaks the pattern (should be 65). Key Learning Point: The wrong term can appear anywhere in the series, including the very last position – always check every term.", "MEDIUM"),
        # Q22
        ("Find the next term: 2, 5, 11, 23, 47, ?",
         ["93", "94", "95", "96"], 2,
         "Pattern: ×2+1 each time. 47×2+1 = 95. Key Learning Point: Verify a “×constant + constant” pattern against all given terms before applying it to find the next one.", "MEDIUM"),
        # Q23
        ("Find the next term: 121, 144, 169, 196, ?",
         ["216", "221", "225", "230"], 2,
         "Perfect squares: 11², 12², 13², 14², 15² = 225. Key Learning Point: Recognise large perfect squares by checking if the number’s square root is a whole number.", "EASY"),
        # Q24
        ("Find the next term: 3, 7, 15, 31, 63, ?",
         ["123", "125", "127", "129"], 2,
         "Pattern: ×2+1 each time. 63×2+1 = 127. Key Learning Point: A “×2+1” pattern produces numbers close to but not exactly double the previous term – verify carefully rather than estimating.", "MEDIUM"),
        # Q25
        ("Find the missing term: 4, 3, 8, 6, 16, 9, 32, ?",
         ["11", "12", "13", "18"], 1,
         "Odd positions (1st,3rd,5th,7th): 4, 8, 16, 32 (×2 each). Even positions (2nd,4th,6th,8th): 3, 6, 9, ? (+3 each) → 12. Key Learning Point: In two-interleaved series, the two sub-series can follow entirely different pattern types (here, geometric and arithmetic).", "MEDIUM")
    ]

    # 25 Worked Examples (Tamil)
    worked_ta = [
        # Q1
        ("அடுத்த உறுப்பைக் காண்க: 2, 4, 6, 8, ?",
         ["9", "10", "11", "12"], 1,
         "மாறா வித்தியாசம் +2. 8+2 = 10. முக்கியக் கற்றல் கருத்து: எளிய அமைப்பு என்பதால், எப்போதும் முதலில் மாறா வித்தியாசத்தை (கூட்டுத் தொடர்) சரிபார்க்கவும்."),
        # Q2
        ("அடுத்த உறுப்பைக் காண்க: 5, 10, 15, 20, ?",
         ["22", "24", "25", "30"], 2,
         "மாறா வித்தியாசம் +5. 20+5 = 25. முக்கியக் கற்றல் கருத்து: கூட்டுத் தொடரில், அடுத்தடுத்த ஒவ்வோர் உறுப்பு இணைக்கும் இடையிலான வித்தியாசம் ஒன்றே."),
        # Q3
        ("அடுத்த உறுப்பைக் காண்க: 3, 6, 12, 24, ?",
         ["36", "42", "48", "50"], 2,
         "மாறா விகிதம் ×2. 24×2 = 48. முக்கியக் கற்றல் கருத்து: வித்தியாசம் மாறாமல் இல்லையெனில், அடுத்தடுத்த உறுப்புகளுக்கிடையிலான விகிதம் மாறாமல் உள்ளதா (பெருக்குத் தொடர்) எனச் சரிபார்க்கவும்."),
        # Q4
        ("அடுத்த உறுப்பைக் காண்க: 100, 90, 80, 70, ?",
         ["55", "60", "65", "68"], 1,
         "மாறா வித்தியாசம் −10. 70−10 = 60. முக்கியக் கற்றல் கருத்து: குறையும் கூட்டுத் தொடர்களும் அதிகரிக்கும் தொடர்களின் அதே தர்க்கத்தைப் பின்பற்றுகின்றன; மாறா வித்தியாசம் மட்டும் எதிர்மறையாக இருக்கும்."),
        # Q5
        ("அடுத்த உறுப்பைக் காண்க: 1, 4, 9, 16, ?",
         ["20", "22", "24", "25"], 3,
         "இவை முழு வர்க்கங்கள்: 1², 2², 3², 4², 5² = 25. முக்கியக் கற்றல் கருத்து: ஒவ்வோர் உறுப்பும் ஒரு முழு எண்ணின் வர்க்கமா எனச் சரிபார்த்து முழு வர்க்கத் தொடர்களை அடையாளம் காணவும்."),
        # Q6
        ("அடுத்த உறுப்பைக் காண்க: 2, 6, 12, 20, 30, ?",
         ["40", "41", "42", "44"], 2,
         "வித்தியாசங்கள்: 4, 6, 8, 10, 12 (ஒவ்வொரு முறையும் 2 அதிகரிக்கிறது). 30+12 = 42. அமைப்பு: n=1,2,3… க்கு n(n+1) → 1×2, 2×3, 3×4, 4×5, 5×6, 6×7=42. முக்கியக் கற்றல் கருத்து: வித்தியாசமே ஒரு மாறா அளவில் அதிகரிக்கும்போது, அமைப்பை வெளிப்படுத்த வித்தியாசங்களைத் தனி வரிசையாக எழுதவும்."),
        # Q7
        ("அடுத்த உறுப்பைக் காண்க: 7, 14, 28, 56, ?",
         ["100", "108", "110", "112"], 3,
         "மாறா விகிதம் ×2. 56×2 = 112. முக்கியக் கற்றல் கருத்து: ஊகித்த விகிதத்தை அமைப்பாக இறுதி செய்யும் முன், அடுத்தடுத்த ஒவ்வோர் இணையுடனும் சரிபார்க்கவும்."),
        # Q8
        ("அடுத்த உறுப்பைக் காண்க: 3, 8, 15, 24, 35, ?",
         ["46", "47", "48", "50"], 2,
         "வித்தியாசங்கள்: 5, 7, 9, 11, 13 (2 அதிகரிக்கிறது). 35+13 = 48. முக்கியக் கற்றல் கருத்து: அதிகரிக்கும் ஒற்றை எண் வித்தியாச அமைப்பு பெரும்பாலும் ஒரு பெருக்கல் அல்லது வர்க்க அடிப்படையிலான சூத்திரத்துடன் (இங்கு, n×(n+2)) ஒத்துப்போகிறது."),
        # Q9
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 2, 5, 10, 17, 26, 38, 50",
         ["10", "17", "38", "50"], 2,
         "அமைப்பு: n=1..7 க்கு n²+1 → 2, 5, 10, 17, 26, 37, 50. 38 என்ற உறுப்பு அமைப்பை உடைக்கிறது (37 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: ஊகித்த சூத்திரத்தைக் கொண்டு ஒவ்வோர் இடத்துக்குமான எதிர்பார்க்கப்படும் மதிப்பைக் கணக்கிட்டு, கொடுக்கப்பட்ட தொடருடன் உறுப்புவாரியாக ஒப்பிடவும்."),
        # Q10
        ("அடுத்த உறுப்பைக் காண்க: 1, 1, 2, 3, 5, 8, ?",
         ["11", "12", "13", "14"], 2,
         "ஃபிபோனச்சி அமைப்பு: ஒவ்வோர் உறுப்பும் முந்தைய இரண்டு உறுப்புகளின் கூடுதல். 5+8 = 13. முக்கியக் கற்றல் கருத்து: ஃபிபோனச்சி வகைத் தொடரில், ஒவ்வோர் உறுப்பும் அதற்கு முந்தைய இரண்டு உறுப்புகளின் கூடுதலுக்குச் சமமா எனச் சரிபார்க்கவும்."),
        # Q11
        ("அடுத்த உறுப்பைக் காண்க: 2, 3, 5, 7, 11, ?",
         ["12", "13", "14", "15"], 1,
         "இவை வரிசையான பகா எண்கள். 11-க்குப்பின் வரும் பகா எண் 13. முக்கியக் கற்றல் கருத்து: கூட்டு அல்லது பெருக்கு அமைப்பு பொருந்தவில்லையெனில், தொடர் பகா எண்களால் ஆனதா எனச் சரிபார்க்கவும்."),
        # Q12
        ("அடுத்த உறுப்பைக் காண்க: 4, 9, 16, 25, 36, ?",
         ["42", "45", "47", "49"], 3,
         "2²-இலிருந்து தொடங்கும் முழு வர்க்கங்கள்: 2², 3², 4², 5², 6², 7² = 49. முக்கியக் கற்றல் கருத்து: வர்க்கத் தொடர் எப்போதும் 1²-இலிருந்து தொடங்குவதில்லை – தொடக்கப் புள்ளியைக் கவனமாகச் சரிபார்க்கவும்."),
        # Q13
        ("அடுத்த உறுப்பைக் காண்க: 1, 8, 27, 64, ?",
         ["100", "110", "121", "125"], 3,
         "முழுக் கனங்கள்: 1³, 2³, 3³, 4³, 5³ = 125. முக்கியக் கற்றல் கருத்து: வர்க்கங்கள் பொருந்தவில்லையெனில், தொடர் முழுக் கனங்களால் ஆனதா எனச் சரிபார்க்கவும்."),
        # Q14
        ("அடுத்த உறுப்பைக் காண்க: 5, 10, 9, 18, 17, 34, ?",
         ["32", "33", "35", "68"], 1,
         "மாறி மாறி வரும் செயல்கள்: ×2, −1, மீண்டும் மீண்டும். 5×2=10, 10−1=9, 9×2=18, 18−1=17, 17×2=34, 34−1=33. முக்கியக் கற்றல் கருத்து: ஒரே செயல் பொருந்தாதபோது, இரண்டு செயல்கள் மீண்டும் வரும் இணையாக மாறி மாறி வருகின்றனவா எனச் சரிபார்க்கவும்."),
        # Q15
        ("விடுபட்ட உறுப்பைக் காண்க: 3, 10, 7, 12, 11, 14, 15, ?",
         ["15", "16", "17", "18"], 1,
         "ஒற்றை இடங்கள் (1, 3, 5, 7-ஆவது): 3, 7, 11, 15 (ஒவ்வொன்றும் +4). இரட்டை இடங்கள் (2, 4, 6, 8-ஆவது): 10, 12, 14, ? (ஒவ்வொன்றும் +2) → 16. முக்கியக் கற்றல் கருத்து: அமைப்பைத் தேடும் முன், இரு இடையிட்ட தொடரை அதன் ஒற்றை இட மற்றும் இரட்டை இட உட்தொடர்களாகப் பிரிக்கவும்."),
        # Q16
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 6, 12, 24, 50, 96, 192",
         ["12", "24", "50", "96"], 2,
         "அமைப்பு: முழுவதும் ×2 → 6, 12, 24, 48, 96, 192. 50 என்ற உறுப்பு அமைப்பை உடைக்கிறது (48 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: முதல் சில உறுப்புகளைக் கொண்டு விகித அமைப்பு உறுதியானதும், பொருந்தாததைக் கண்டறிய முழு எதிர்பார்க்கப்படும் தொடரைக் கணக்கிடவும்."),
        # Q17
        ("அடுத்த உறுப்பைக் காண்க: 8, 12, 9, 13, 10, 14, ?",
         ["10", "11", "15", "18"], 1,
         "மாறி மாறி வரும் செயல்கள்: +4, −3, மீண்டும் மீண்டும். 14−3 = 11. முக்கியக் கற்றல் கருத்து: மாறி மாறி வரும் தொடர்களில், அடுத்த உறுப்பை முன்கணிக்கும் முன் மீண்டும் வரும் இணையின் இரு செயல்களையும் கண்டறியவும்."),
        # Q18
        ("அடுத்த உறுப்பைக் காண்க: 2, 6, 18, 54, ?",
         ["108", "144", "162", "180"], 2,
         "மாறா விகிதம் ×3. 54×3 = 162. முக்கியக் கற்றல் கருத்து: பெருக்குத் தொடருக்கு ×2 பொருந்தவில்லையெனில், ×3 போன்ற பிற மாறா விகிதங்களைச் சோதிக்கவும்."),
        # Q19
        ("அடுத்த உறுப்பைக் காண்க: 100, 50, 25, 12.5, ?",
         ["5", "6", "6.25", "6.5"], 2,
         "மாறா விகிதம் ÷2. 12.5÷2 = 6.25. முக்கியக் கற்றல் கருத்து: பெருக்குத் தொடர்களில் முழு எண் விகிதங்கள் மட்டுமல்லாமல் பின்ன அல்லது தசம விகிதங்களும் இருக்கலாம்."),
        # Q20
        ("அடுத்த உறுப்பைக் காண்க: 1, 4, 10, 22, 46, ?",
         ["90", "92", "94", "96"], 2,
         "அமைப்பு: ஒவ்வோர் உறுப்பும் = 2×(முந்தைய உறுப்பு)+2. 46×2+2 = 94. முக்கியக் கற்றல் கருத்து: மாறா வித்தியாசமோ மாறா விகிதமோ தனியாகப் பொருந்தாதபோது, “×2, பின்னர் ஒரு மாறிலியைக் கூட்டு” போன்ற இணைந்த செயலைச் சோதிக்கவும்."),
        # Q21
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 5, 10, 17, 26, 37, 50, 64",
         ["17", "26", "50", "64"], 3,
         "அமைப்பு: n=2..8 க்கு n²+1 → 5, 10, 17, 26, 37, 50, 65. 64 என்ற உறுப்பு அமைப்பை உடைக்கிறது (65 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: தவறான உறுப்பு கடைசி இடம் உட்படத் தொடரின் எந்த இடத்திலும் வரலாம் – எப்போதும் ஒவ்வோர் உறுப்பையும் சரிபார்க்கவும்."),
        # Q22
        ("அடுத்த உறுப்பைக் காண்க: 2, 5, 11, 23, 47, ?",
         ["93", "94", "95", "96"], 2,
         "அமைப்பு: ஒவ்வொரு முறையும் ×2+1. 47×2+1 = 95. முக்கியக் கற்றல் கருத்து: அடுத்த உறுப்பைக் காணப் பயன்படுத்தும் முன், “×மாறிலி + மாறிலி” அமைப்பைக் கொடுக்கப்பட்ட அனைத்து உறுப்புகளுடனும் சரிபார்க்கவும்."),
        # Q23
        ("அடுத்த உறுப்பைக் காண்க: 121, 144, 169, 196, ?",
         ["216", "221", "225", "230"], 2,
         "முழு வர்க்கங்கள்: 11², 12², 13², 14², 15² = 225. முக்கியக் கற்றல் கருத்து: எண்ணின் வர்க்கமூலம் ஒரு முழு எண்ணா எனச் சரிபார்த்துப் பெரிய முழு வர்க்கங்களை அடையாளம் காணவும்."),
        # Q24
        ("அடுத்த உறுப்பைக் காண்க: 3, 7, 15, 31, 63, ?",
         ["123", "125", "127", "129"], 2,
         "அமைப்பு: ஒவ்வொரு முறையும் ×2+1. 63×2+1 = 127. முக்கியக் கற்றல் கருத்து: “×2+1” அமைப்பு முந்தைய உறுப்பின் இருமடங்குக்கு அருகில் ஆனால் சரியாக இருமடங்கல்லாத எண்களைத் தருகிறது – தோராயமாக்காமல் கவனமாகச் சரிபார்க்கவும்."),
        # Q25
        ("விடுபட்ட உறுப்பைக் காண்க: 4, 3, 8, 6, 16, 9, 32, ?",
         ["11", "12", "13", "18"], 1,
         "ஒற்றை இடங்கள் (1, 3, 5, 7-ஆவது): 4, 8, 16, 32 (ஒவ்வொன்றும் ×2). இரட்டை இடங்கள் (2, 4, 6, 8-ஆவது): 3, 6, 9, ? (ஒவ்வொன்றும் +3) → 12. முக்கியக் கற்றல் கருத்து: இரு இடையிட்ட தொடர்களில், இரு உட்தொடர்களும் முற்றிலும் வேறுபட்ட அமைப்பு வகைகளைத் (இங்கு, பெருக்கு மற்றும் கூட்டு) பின்பற்றலாம்.")
    ]

    # 30 Independent Practice (English)
    indep_en = [
        # Q1
        ("Find the next term: 3, 6, 9, 12, ?",
         ["13", "14", "15", "16"], 2,
         "Constant difference +3. 12+3 = 15. Key Learning Point: Check for a constant difference first.", "EASY"),
        # Q2
        ("Find the next term: 4, 8, 12, 16, ?",
         ["18", "20", "22", "24"], 1,
         "Constant difference +4. 16+4 = 20. Key Learning Point: Constant-difference series are the simplest pattern to verify.", "EASY"),
        # Q3
        ("Find the next term: 5, 15, 45, 135, ?",
         ["270", "315", "405", "450"], 2,
         "Constant ratio ×3. 135×3 = 405. Key Learning Point: Check the ratio between consecutive terms when the difference is not constant.", "EASY"),
        # Q4
        ("Find the next term: 90, 80, 70, 60, ?",
         ["45", "50", "55", "58"], 1,
         "Constant difference −10. 60−10 = 50. Key Learning Point: A decreasing arithmetic series has a constant negative difference.", "EASY"),
        # Q5
        ("Find the next term: 1, 9, 25, 49, ?",
         ["64", "72", "81", "90"], 2,
         "Squares of odd numbers: 1², 3², 5², 7², 9² = 81. Key Learning Point: Some square series only include odd-numbered or even-numbered bases – check the base pattern, not just the results.", "EASY"),
        # Q6
        ("Find the next term: 4, 10, 25, 62.5, ?",
         ["125", "150", "156.25", "160"], 2,
         "Constant ratio ×2.5. 62.5 × 2.5 = 156.25. Key Learning Point: Divide consecutive terms to find the ratio – it can be a decimal such as 2.5.", "MEDIUM"),
        # Q7
        ("Find the next term: 5, 11, 19, 29, 41, ?",
         ["53", "55", "57", "59"], 1,
         "Differences: 6, 8, 10, 12, 14 (increasing by 2). 41+14 = 55. Key Learning Point: Write out the row of differences to reveal an increasing-gap pattern.", "EASY"),
        # Q8
        ("Find the next term: 729, 243, 81, 27, ?",
         ["6", "9", "12", "18"], 1,
         "Constant ratio ÷3. 27 ÷ 3 = 9. Key Learning Point: A geometric series can decrease – check for division by a constant as well as multiplication.", "EASY"),
        # Q9
        ("Find the next term: 2, 7, 17, 37, 77, ?",
         ["150", "153", "155", "157"], 3,
         "Pattern: ×2+3 each time. 77×2+3 = 157. Key Learning Point: Test combined “×constant + constant” patterns when a simple ratio doesn’t fit exactly.", "MEDIUM"),
        # Q10
        ("Find the wrong number in the series: 8, 16, 32, 72, 128, 256",
         ["16", "32", "72", "128"], 2,
         "Pattern: ×2 throughout → 8, 16, 32, 64, 128, 256. The term 72 breaks the pattern (should be 64). Key Learning Point: Compute the fully expected series before comparing it term by term against the given one.", "MEDIUM"),
        # Q11
        ("Find the next term: 2, 1, 3, 4, 7, 11, ?",
         ["16", "17", "18", "19"], 2,
         "Each term is the sum of the two preceding terms (Fibonacci-type). 7+11 = 18. Key Learning Point: Fibonacci-type series can start with any two numbers, not just 1 and 1.", "EASY"),
        # Q12
        ("Find the next term: 13, 17, 19, 23, 29, ?",
         ["29", "30", "31", "33"], 2,
         "Prime numbers in order. The next prime after 29 is 31. Key Learning Point: If differences look irregular, check whether the terms are all prime numbers.", "EASY"),
        # Q13
        ("Find the next term: 2, 7, 14, 23, 34, ?",
         ["45", "46", "47", "49"], 2,
         "Pattern: n² − 2 for n = 2, 3, 4, … → 4−2, 9−2, 16−2, 25−2, 36−2, 49−2 = 47. Key Learning Point: Numbers just below perfect squares suggest an “n² − constant” pattern.", "EASY"),
        # Q14
        ("Find the next term: 8, 27, 64, 125, ?",
         ["196", "200", "216", "220"], 2,
         "Perfect cubes starting from 2³: 2³, 3³, 4³, 5³, 6³ = 216. Key Learning Point: A cube series does not always begin at 1³ – verify the starting base.", "EASY"),
        # Q15
        ("Find the next term: 2, 6, 4, 12, 10, 30, ?",
         ["26", "28", "32", "90"], 1,
         "Alternating operations: ×3, −2, repeating. 2×3=6, 6−2=4, 4×3=12, 12−2=10, 10×3=30, 30−2=28. Key Learning Point: The two alternating operations can be of different types (multiply and subtract) – identify both before continuing.", "MEDIUM"),
        # Q16
        ("Find the missing term: 4, 9, 8, 13, 12, 17, 16, ?",
         ["19", "20", "21", "22"], 2,
         "Odd positions: 4, 8, 12, 16 (+4 each). Even positions: 9, 13, 17, ? (+4 each) → 21. Key Learning Point: Both sub-series in a two-interleaved series can share the same type of pattern with different starting points.", "MEDIUM"),
        # Q17
        ("Find the wrong number in the series: 1, 3, 7, 13, 21, 32, 43",
         ["7", "13", "21", "32"], 3,
         "Differences should increase by 2: 2, 4, 6, 8, 10, 12 → 1, 3, 7, 13, 21, 31, 43. The term 32 breaks the pattern (should be 31). Key Learning Point: In wrong-number questions, the row of differences often shows where the pattern breaks – look for the difference that is out of step.", "MEDIUM"),
        # Q18
        ("Find the next term: 10, 15, 11, 16, 12, 17, ?",
         ["12", "13", "18", "22"], 1,
         "Alternating operations: +5, −4, repeating. 17−4 = 13. Key Learning Point: Track which operation applies at each step of an alternating series rather than assuming the last one repeats.", "EASY"),
        # Q19
        ("Find the next term: 16, 24, 36, 54, ?",
         ["72", "78", "81", "90"], 2,
         "Constant ratio ×1.5 (that is, ×3/2): 16×1.5=24, 24×1.5=36, 36×1.5=54, 54×1.5=81. Key Learning Point: The common ratio need not be a whole number – divide consecutive terms to find it.", "MEDIUM"),
        # Q20
        ("Find the next term: 1, 2, 6, 24, 120, ?",
         ["600", "720", "840", "960"], 1,
         "The multipliers increase by 1: ×2, ×3, ×4, ×5, ×6. 120 × 6 = 720. Key Learning Point: If the ratio between terms keeps changing, write the ratios as a row – they may form their own simple pattern.", "EASY"),
        # Q21
        ("Find the next term: 2, 5, 14, 41, 122, ?",
         ["363", "365", "367", "369"], 1,
         "Pattern: ×3 − 1 each time. 122 × 3 − 1 = 365. Key Learning Point: When terms roughly triple, test “×3 plus or minus a constant” and check it on every term.", "MEDIUM"),
        # Q22
        ("Find the wrong number in the series: 3, 6, 11, 18, 28, 38",
         ["6", "11", "18", "28"], 3,
         "Pattern: n²+2 for n=1..6 → 3, 6, 11, 18, 27, 38. The term 28 breaks the pattern (should be 27). Key Learning Point: Compute the formula-based expected value for every term, not just the ones that look suspicious.", "MEDIUM"),
        # Q23
        ("Find the next term: 1, 1, 2, 4, 7, 13, ?",
         ["20", "22", "24", "26"], 2,
         "Each term is the sum of the three preceding terms: 1+1+2=4, 1+2+4=7, 2+4+7=13, 4+7+13=24. Key Learning Point: If adding the last two terms does not work, try adding the last three.", "MEDIUM"),
        # Q24
        ("Find the missing term: 5, 10, 20, 40, ?, 160",
         ["60", "70", "80", "90"], 2,
         "Constant ratio ×2 throughout. 40×2 = 80 (and 80×2 = 160, confirming the pattern). Key Learning Point: For a missing middle term, verify your answer against the term that follows it, not just the one before it.", "EASY"),
        # Q25
        ("Find the next term: 1, 2, 4, 7, 11, 16, ?",
         ["20", "21", "22", "23"], 2,
         "Differences: 1, 2, 3, 4, 5, 6. 16 + 6 = 22. Key Learning Point: Differences that increase by 1 each time are a common pattern – write out the row of differences to spot it.", "EASY"),
        # Q26
        ("Find the missing term: 5, 20, 10, 25, 15, 30, 20, ?",
         ["25", "30", "35", "40"], 2,
         "Odd positions: 5, 10, 15, 20 (+5 each). Even positions: 20, 25, 30, ? (+5 each) → 35. Key Learning Point: Both odd-position and even-position sub-series can share the same step size but different starting values.", "MEDIUM"),
        # Q27
        ("Find the missing term: 1, 2, 5, 10, ?, 26",
         ["15", "16", "17", "18"], 2,
         "Differences: 1, 3, 5, 7, 9 (consecutive odd numbers). 10 + 7 = 17, and 17 + 9 = 26 confirms it. Key Learning Point: For a missing middle term, check that the value fits the difference pattern on both sides.", "EASY"),
        # Q28
        ("Find the next term: 20, 17, 20, 15, 20, 13, ?",
         ["11", "20", "9", "13"], 1,
         "Odd positions are constant at 20. Even positions decrease by 2 (17, 15, 13…). The 7th term (odd position) = 20. Key Learning Point: In an alternating-position series, one sub-series may be constant while the other changes – identify each independently.", "MEDIUM"),
        # Q29
        ("Find the next term: 2, 9, 28, 65, 126, ?",
         ["215", "216", "217", "225"], 2,
         "Pattern: n³ + 1 → 1³+1, 2³+1, 3³+1, 4³+1, 5³+1, 6³+1 = 217. Key Learning Point: Numbers just above (or below) perfect cubes suggest an “n³ ± constant” pattern.", "MEDIUM"),
        # Q30
        ("Find the wrong number in the series: 2, 3, 5, 7, 11, 15, 17",
         ["5", "11", "15", "17"], 2,
         "These should be consecutive prime numbers: 2, 3, 5, 7, 11, 13, 17. 15 = 3 × 5 is not prime (should be 13). Key Learning Point: In a prime series, test each term for divisibility – any composite number is the wrong term.", "EASY")
    ]

    # 30 Independent Practice (Tamil)
    indep_ta = [
        # Q1
        ("அடுத்த உறுப்பைக் காண்க: 3, 6, 9, 12, ?",
         ["13", "14", "15", "16"], 2,
         "மாறா வித்தியாசம் +3. 12+3 = 15. முக்கியக் கற்றல் கருத்து: முதலில் மாறா வித்தியாசத்தைச் சரிபார்க்கவும்."),
        # Q2
        ("அடுத்த உறுப்பைக் காண்க: 4, 8, 12, 16, ?",
         ["18", "20", "22", "24"], 1,
         "மாறா வித்தியாசம் +4. 16+4 = 20. முக்கியக் கற்றல் கருத்து: மாறா வித்தியாசத் தொடர்களே சரிபார்க்க எளிய அமைப்பு."),
        # Q3
        ("அடுத்த உறுப்பைக் காண்க: 5, 15, 45, 135, ?",
         ["270", "315", "405", "450"], 2,
         "மாறா விகிதம் ×3. 135×3 = 405. முக்கியக் கற்றல் கருத்து: வித்தியாசம் மாறாமல் இல்லாதபோது, அடுத்தடுத்த உறுப்புகளுக்கிடையிலான விகிதத்தைச் சரிபார்க்கவும்."),
        # Q4
        ("அடுத்த உறுப்பைக் காண்க: 90, 80, 70, 60, ?",
         ["45", "50", "55", "58"], 1,
         "மாறா வித்தியாசம் −10. 60−10 = 50. முக்கியக் கற்றல் கருத்து: குறையும் கூட்டுத் தொடருக்கு எதிர்மறை மாறா வித்தியாசம் உண்டு."),
        # Q5
        ("அடுத்த உறுப்பைக் காண்க: 1, 9, 25, 49, ?",
         ["64", "72", "81", "90"], 2,
         "ஒற்றை எண்களின் வர்க்கங்கள்: 1², 3², 5², 7², 9² = 81. முக்கியக் கற்றல் கருத்து: சில வர்க்கத் தொடர்கள் ஒற்றை அல்லது இரட்டை அடிமானங்களை மட்டுமே கொண்டிருக்கும் – விளைவுகளை மட்டுமல்லாமல் அடிமான அமைப்பையும் சரிபார்க்கவும்."),
        # Q6
        ("அடுத்த உறுப்பைக் காண்க: 4, 10, 25, 62.5, ?",
         ["125", "150", "156.25", "160"], 2,
         "மாறா விகிதம் ×2.5. 62.5 × 2.5 = 156.25. முக்கியக் கற்றல் கருத்து: விகிதத்தைக் காண அடுத்தடுத்த உறுப்புகளை வகுக்கவும் – அது 2.5 போன்ற தசம எண்ணாகவும் இருக்கலாம்."),
        # Q7
        ("அடுத்த உறுப்பைக் காண்க: 5, 11, 19, 29, 41, ?",
         ["53", "55", "57", "59"], 1,
         "வித்தியாசங்கள்: 6, 8, 10, 12, 14 (2 அதிகரிக்கிறது). 41+14 = 55. முக்கியக் கற்றல் கருத்து: அதிகரிக்கும் இடைவெளி அமைப்பை வெளிப்படுத்த வித்தியாசங்களின் வரிசையை எழுதவும்."),
        # Q8
        ("அடுத்த உறுப்பைக் காண்க: 729, 243, 81, 27, ?",
         ["6", "9", "12", "18"], 1,
         "மாறா விகிதம் ÷3. 27 ÷ 3 = 9. முக்கியக் கற்றல் கருத்து: பெருக்குத் தொடர் குறையவும் செய்யலாம் – ஒரு மாறிலியால் பெருக்குவதை மட்டுமல்லாமல் வகுப்பதையும் சரிபார்க்கவும்."),
        # Q9
        ("அடுத்த உறுப்பைக் காண்க: 2, 7, 17, 37, 77, ?",
         ["150", "153", "155", "157"], 3,
         "அமைப்பு: ஒவ்வொரு முறையும் ×2+3. 77×2+3 = 157. முக்கியக் கற்றல் கருத்து: எளிய விகிதம் சரியாகப் பொருந்தாதபோது, இணைந்த “×மாறிலி + மாறிலி” அமைப்புகளைச் சோதிக்கவும்."),
        # Q10
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 8, 16, 32, 72, 128, 256",
         ["16", "32", "72", "128"], 2,
         "அமைப்பு: முழுவதும் ×2 → 8, 16, 32, 64, 128, 256. 72 என்ற உறுப்பு அமைப்பை உடைக்கிறது (64 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: கொடுக்கப்பட்ட தொடருடன் உறுப்புவாரியாக ஒப்பிடும் முன், முழு எதிர்பார்க்கப்படும் தொடரைக் கணக்கிடவும்."),
        # Q11
        ("அடுத்த உறுப்பைக் காண்க: 2, 1, 3, 4, 7, 11, ?",
         ["16", "17", "18", "19"], 2,
         "ஒவ்வோர் உறுப்பும் முந்தைய இரண்டு உறுப்புகளின் கூடுதல் (ஃபிபோனச்சி வகை). 7+11 = 18. முக்கியக் கற்றல் கருத்து: ஃபிபோனச்சி வகைத் தொடர் 1 மற்றும் 1 மட்டுமல்லாமல் எந்த இரண்டு எண்களிலிருந்தும் தொடங்கலாம்."),
        # Q12
        ("அடுத்த உறுப்பைக் காண்க: 13, 17, 19, 23, 29, ?",
         ["29", "30", "31", "33"], 2,
         "வரிசையான பகா எண்கள். 29-க்குப்பின் வரும் பகா எண் 31. முக்கியக் கற்றல் கருத்து: வித்தியாசங்கள் ஒழுங்கற்றதாகத் தோன்றினால், உறுப்புகள் அனைத்தும் பகா எண்களா எனச் சரிபார்க்கவும்."),
        # Q13
        ("அடுத்த உறுப்பைக் காண்க: 2, 7, 14, 23, 34, ?",
         ["45", "46", "47", "49"], 2,
         "அமைப்பு: n = 2, 3, 4, … க்கு n² − 2 → 4−2, 9−2, 16−2, 25−2, 36−2, 49−2 = 47. முக்கியக் கற்றல் கருத்து: முழு வர்க்கங்களைவிடச் சற்று குறைவான எண்கள் “n² − மாறிலி” அமைப்பைக் குறிக்கின்றன."),
        # Q14
        ("அடுத்த உறுப்பைக் காண்க: 8, 27, 64, 125, ?",
         ["196", "200", "216", "220"], 2,
         "2³-இலிருந்து தொடங்கும் முழுக் கனங்கள்: 2³, 3³, 4³, 5³, 6³ = 216. முக்கியக் கற்றல் கருத்து: கனத்தொடர் எப்போதும் 1³-இலிருந்து தொடங்குவதில்லை – தொடக்க அடிமானத்தைச் சரிபார்க்கவும்."),
        # Q15
        ("அடுத்த உறுப்பைக் காண்க: 2, 6, 4, 12, 10, 30, ?",
         ["26", "28", "32", "90"], 1,
         "மாறி மாறி வரும் செயல்கள்: ×3, −2, மீண்டும் மீண்டும். 2×3=6, 6−2=4, 4×3=12, 12−2=10, 10×3=30, 30−2=28. முக்கியக் கற்றல் கருத்து: மாறி மாறி வரும் இரு செயல்களும் வெவ்வேறு வகையாக (பெருக்கல் மற்றும் கழித்தல்) இருக்கலாம் – தொடரும் முன் இரண்டையும் கண்டறியவும்."),
        # Q16
        ("விடுபட்ட உறுப்பைக் காண்க: 4, 9, 8, 13, 12, 17, 16, ?",
         ["19", "20", "21", "22"], 2,
         "ஒற்றை இடங்கள்: 4, 8, 12, 16 (ஒவ்வொன்றும் +4). இரட்டை இடங்கள்: 9, 13, 17, ? (ஒவ்வொன்றும் +4) → 21. முக்கியக் கற்றல் கருத்து: இரு இடையிட்ட தொடரின் இரு உட்தொடர்களும் வெவ்வேறு தொடக்கப் புள்ளிகளுடன் ஒரே வகை அமைப்பைக் கொண்டிருக்கலாம்."),
        # Q17
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 1, 3, 7, 13, 21, 32, 43",
         ["7", "13", "21", "32"], 3,
         "வித்தியாசங்கள் 2 அதிகரிக்க வேண்டும்: 2, 4, 6, 8, 10, 12 → 1, 3, 7, 13, 21, 31, 43. 32 என்ற உறுப்பு அமைப்பை உடைக்கிறது (31 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: தவறான எண் வினாக்களில், வித்தியாசங்களின் வரிசை அமைப்பு எங்கு உடைகிறது என்பதைப் பெரும்பாலும் காட்டும் – ஒழுங்கிலிருந்து விலகும் வித்தியாசத்தைத் தேடவும்."),
        # Q18
        ("அடுத்த உறுப்பைக் காண்க: 10, 15, 11, 16, 12, 17, ?",
         ["12", "13", "18", "22"], 1,
         "மாறி மாறி வரும் செயல்கள்: +5, −4, மீண்டும் மீண்டும். 17−4 = 13. முக்கியக் கற்றல் கருத்து: கடைசிச் செயலே மீண்டும் வரும் எனக் கருதாமல், மாறி மாறி வரும் தொடரின் ஒவ்வொரு படியிலும் எந்தச் செயல் பொருந்துகிறது எனப் பின்தொடரவும்."),
        # Q19
        ("அடுத்த உறுப்பைக் காண்க: 16, 24, 36, 54, ?",
         ["72", "78", "81", "90"], 2,
         "மாறா விகிதம் ×1.5 (அதாவது, ×3/2): 16×1.5=24, 24×1.5=36, 36×1.5=54, 54×1.5=81. முக்கியக் கற்றல் கருத்து: பொது விகிதம் முழு எண்ணாக இருக்க வேண்டியதில்லை – அதைக் காண அடுத்தடுத்த உறுப்புகளை வகுக்கவும்."),
        # Q20
        ("அடுத்த உறுப்பைக் காண்க: 1, 2, 6, 24, 120, ?",
         ["600", "720", "840", "960"], 1,
         "பெருக்கிகள் 1 அதிகரிக்கின்றன: ×2, ×3, ×4, ×5, ×6. 120 × 6 = 720. முக்கியக் கற்றல் கருத்து: உறுப்புகளுக்கிடையிலான விகிதம் மாறிக்கொண்டே இருந்தால், விகிதங்களை ஒரு வரிசையாக எழுதவும் – அவை தமக்கென ஓர் எளிய அமைப்பை உருவாக்கலாம்."),
        # Q21
        ("அடுத்த உறுப்பைக் காண்க: 2, 5, 14, 41, 122, ?",
         ["363", "365", "367", "369"], 1,
         "அமைப்பு: ஒவ்வொரு முறையும் ×3 − 1. 122 × 3 − 1 = 365. முக்கியக் கற்றல் கருத்து: உறுப்புகள் ஏறத்தாழ மும்மடங்காகும்போது, “×3 கூட்டல் அல்லது கழித்தல் ஒரு மாறிலி” என்பதைச் சோதித்து, ஒவ்வோர் உறுப்புடனும் சரிபார்க்கவும்."),
        # Q22
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 3, 6, 11, 18, 28, 38",
         ["6", "11", "18", "28"], 3,
         "அமைப்பு: n=1..6 க்கு n²+2 → 3, 6, 11, 18, 27, 38. 28 என்ற உறுப்பு அமைப்பை உடைக்கிறது (27 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: சந்தேகத்துக்குரியதாகத் தோன்றும் உறுப்புகளுக்கு மட்டுமல்லாமல், ஒவ்வோர் உறுப்புக்குமான சூத்திர அடிப்படையிலான எதிர்பார்க்கப்படும் மதிப்பைக் கணக்கிடவும்."),
        # Q23
        ("அடுத்த உறுப்பைக் காண்க: 1, 1, 2, 4, 7, 13, ?",
         ["20", "22", "24", "26"], 2,
         "ஒவ்வோர் உறுப்பும் முந்தைய மூன்று உறுப்புகளின் கூடுதல்: 1+1+2=4, 1+2+4=7, 2+4+7=13, 4+7+13=24. முக்கியக் கற்றல் கருத்து: கடைசி இரண்டு உறுப்புகளைக் கூட்டுவது பொருந்தவில்லையெனில், கடைசி மூன்றைக் கூட்டிப் பார்க்கவும்."),
        # Q24
        ("விடுபட்ட உறுப்பைக் காண்க: 5, 10, 20, 40, ?, 160",
         ["60", "70", "80", "90"], 2,
         "முழுவதும் மாறா விகிதம் ×2. 40×2 = 80 (மேலும் 80×2 = 160 என்பது அமைப்பை உறுதிசெய்கிறது). முக்கியக் கற்றல் கருத்து: நடுவில் விடுபட்ட உறுப்புக்கு, விடையை அதற்கு முந்தைய உறுப்புடன் மட்டுமல்லாமல் அடுத்த உறுப்புடனும் சரிபார்க்கவும்."),
        # Q25
        ("அடுத்த உறுப்பைக் காண்க: 1, 2, 4, 7, 11, 16, ?",
         ["20", "21", "22", "23"], 2,
         "வித்தியாசங்கள்: 1, 2, 3, 4, 5, 6. 16 + 6 = 22. முக்கியக் கற்றல் கருத்து: ஒவ்வொரு முறையும் 1 அதிகரிக்கும் வித்தியாசங்கள் ஒரு பொதுவான அமைப்பாகும் – அதைக் கண்டறிய வித்தியாசங்களின் வரிசையை எழுதவும்."),
        # Q26
        ("விடுபட்ட உறுப்பைக் காண்க: 5, 20, 10, 25, 15, 30, 20, ?",
         ["25", "30", "35", "40"], 2,
         "ஒற்றை இடங்கள்: 5, 10, 15, 20 (ஒவ்வொன்றும் +5). இரட்டை இடங்கள்: 20, 25, 30, ? (ஒவ்வொன்றும் +5) → 35. முக்கியக் கற்றல் கருத்து: ஒற்றை இட மற்றும் இரட்டை இட உட்தொடர்கள் இரண்டும் ஒரே படி அளவையும் வெவ்வேறு தொடக்க மதிப்புகளையும் கொண்டிருக்கலாம்."),
        # Q27
        ("விடுபட்ட உறுப்பைக் காண்க: 1, 2, 5, 10, ?, 26",
         ["15", "16", "17", "18"], 2,
         "வித்தியாசங்கள்: 1, 3, 5, 7, 9 (அடுத்தடுத்த ஒற்றை எண்கள்). 10 + 7 = 17; மேலும் 17 + 9 = 26 என்பது இதை உறுதிசெய்கிறது. முக்கியக் கற்றல் கருத்து: நடுவில் விடுபட்ட உறுப்புக்கு, அம்மதிப்பு இருபுறமும் வித்தியாச அமைப்புக்குப் பொருந்துகிறதா எனச் சரிபார்க்கவும்."),
        # Q28
        ("அடுத்த உறுப்பைக் காண்க: 20, 17, 20, 15, 20, 13, ?",
         ["11", "20", "9", "13"], 1,
         "ஒற்றை இடங்கள் 20 என மாறாமல் உள்ளன. இரட்டை இடங்கள் 2 குறைகின்றன (17, 15, 13…). 7-ஆவது உறுப்பு (ஒற்றை இடம்) = 20. முக்கியக் கற்றல் கருத்து: மாற்று இடத் தொடரில், ஓர் உட்தொடர் மாறாமல் இருக்க, மற்றொன்று மாறலாம் – ஒவ்வொன்றையும் தனித்தனியாகக் கண்டறியவும்."),
        # Q29
        ("அடுத்த உறுப்பைக் காண்க: 2, 9, 28, 65, 126, ?",
         ["215", "216", "217", "225"], 2,
         "அமைப்பு: n³ + 1 → 1³+1, 2³+1, 3³+1, 4³+1, 5³+1, 6³+1 = 217. முக்கியக் கற்றல் கருத்து: முழுக் கனங்களைவிடச் சற்று அதிகமான (அல்லது குறைவான) எண்கள் “n³ ± மாறிலி” அமைப்பைக் குறிக்கின்றன."),
        # Q30
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 2, 3, 5, 7, 11, 15, 17",
         ["5", "11", "15", "17"], 2,
         "இவை அடுத்தடுத்த பகா எண்களாக இருக்க வேண்டும்: 2, 3, 5, 7, 11, 13, 17. 15 = 3 × 5 பகா எண் அல்ல (13 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: பகா எண் தொடரில், ஒவ்வோர் உறுப்பையும் வகுபடுதன்மைக்குச் சோதிக்கவும் – எந்தப் பகு எண்ணும் தவறான உறுப்பாகும்.")
    ]

    # 30 Assessment Questions (English)
    assess_en = [
        # Q1
        ("Find the next term: 8, 16, 24, 32, ?",
         ["36", "38", "40", "42"], 2,
         "Constant difference +8. 32 + 8 = 40. Key Learning Point: Check for a constant difference first.", "EASY"),
        # Q2
        ("Find the next term: 2, 3, 6, 11, 18, ?",
         ["25", "27", "29", "31"], 1,
         "Differences: 1, 3, 5, 7 (consecutive odd numbers). Next difference = 9: 18 + 9 = 27. Key Learning Point: When the difference is not constant, check whether the differences themselves form a simple series.", "EASY"),
        # Q3
        ("Find the next term: 50, 45, 41, 38, 36, ?",
         ["33", "34", "35", "36"], 2,
         "Differences: −5, −4, −3, −2. Next difference = −1: 36 − 1 = 35. Key Learning Point: A decreasing series may have a gap that shrinks steadily – write out the differences to see it.", "EASY"),
        # Q4
        ("Find the next term: 80, 70, 60, 50, ?",
         ["35", "38", "40", "42"], 2,
         "Constant difference −10. 50 − 10 = 40. Key Learning Point: A decreasing arithmetic series has a constant negative difference.", "EASY"),
        # Q5
        ("Find the next term: 1, 2, 4, 8, 15, 26, ?",
         ["40", "42", "44", "46"], 1,
         "First differences: 1, 2, 4, 7, 11. Second differences: 1, 2, 3, 4 → next = 5, so the next first difference = 16. 26 + 16 = 42. Key Learning Point: If the first differences are not regular, take the differences again – a second-level pattern often appears.", "MEDIUM"),
        # Q6
        ("Find the next term: 1, 2, 6, 12, 36, 72, ?",
         ["144", "180", "216", "288"], 2,
         "Alternating multiplication: ×2, ×3, repeating. 72 × 3 = 216. Key Learning Point: A geometric-type series may alternate between two different multipliers.", "MEDIUM"),
        # Q7
        ("Find the next term: 5, 9, 17, 33, 65, ?",
         ["125", "127", "129", "131"], 2,
         "Pattern: ×2 − 1 each time. 5×2−1=9, 9×2−1=17, 17×2−1=33, 33×2−1=65, 65×2−1=129. Key Learning Point: Verify a “×constant − constant” pattern against every term before extending it.", "MEDIUM"),
        # Q8
        ("Find the next term: 1, 3, 6, 10, 15, ?",
         ["18", "20", "21", "25"], 2,
         "Differences: 2, 3, 4, 5, 6. 15 + 6 = 21 (these are the triangular numbers). Key Learning Point: Differences that increase by 1 produce the triangular numbers 1, 3, 6, 10, 15, 21…", "EASY"),
        # Q9
        ("Find the next term: 3, 10, 21, 36, 55, ?",
         ["74", "76", "78", "80"], 2,
         "Differences: 7, 11, 15, 19 (increasing by 4). Next difference = 23: 55 + 23 = 78. Key Learning Point: When the differences themselves form an arithmetic series, continue that series to find the next difference.", "EASY"),
        # Q10
        ("Find the wrong number in the series: 1, 8, 27, 65, 125, 216",
         ["8", "27", "65", "125"], 2,
         "Cubes: 1³, 2³, 3³, 4³, 5³, 6³ = 1, 8, 27, 64, 125, 216. The term 65 breaks the pattern (should be 64). Key Learning Point: Once a cube pattern is recognised, compute every expected cube – a term that is one more or less is the trap.", "MEDIUM"),
        # Q11
        ("Find the next term: 3, 4, 7, 11, 18, 29, ?",
         ["44", "45", "46", "47"], 3,
         "Each term is the sum of the two preceding terms: 3+4=7, 4+7=11, 7+11=18, 11+18=29, 18+29=47. Key Learning Point: Fibonacci-type series can start with any two numbers.", "EASY"),
        # Q12
        ("Find the next term: 4, 6, 10, 14, 22, 26, ?",
         ["30", "32", "34", "38"], 2,
         "Each term is twice a prime number: 2×2, 2×3, 2×5, 2×7, 2×11, 2×13. The next prime is 17, so the next term = 2 × 17 = 34. Key Learning Point: If the terms are all even and the gaps are irregular, halve them – a familiar series (here, primes) may appear.", "MEDIUM"),
        # Q13
        ("Find the next term: 1, 8, 9, 64, 25, 216, ?",
         ["36", "49", "343", "512"], 1,
         "Odd positions are squares and even positions are cubes: 1², 2³, 3², 4³, 5², 6³. The 7th term is a square: 7² = 49. Key Learning Point: When squares and cubes appear together, check whether they alternate by position.", "MEDIUM"),
        # Q14
        ("Find the next term: 0, 6, 24, 60, 120, ?",
         ["180", "200", "210", "216"], 2,
         "Pattern: n³ − n → 1−1, 8−2, 27−3, 64−4, 125−5, 216−6 = 210 (Equivalently, the product of three consecutive numbers: 5 × 6 × 7 = 210.) Key Learning Point: Numbers slightly below perfect cubes suggest a cube-based variation such as n³ − n.", "MEDIUM"),
        # Q15
        ("Find the next term: 1, 4, 8, 11, 22, 25, ?",
         ["28", "48", "50", "75"], 2,
         "Alternating operations: +3, ×2, repeating. 1+3=4, 4×2=8, 8+3=11, 11×2=22, 22+3=25, 25×2=50. Key Learning Point: Identify both operations in the repeating pair and track which one applies at the next step.", "MEDIUM"),
        # Q16
        ("Find the missing term: 3, 5, 7, 10, 11, 20, 15, ?",
         ["25", "30", "35", "40"], 3,
         "Odd positions: 3, 7, 11, 15 (+4 each). Even positions: 5, 10, 20, ? (×2 each) → 40. Key Learning Point: The two sub-series of an interleaved series can follow different operations (here, +4 and ×2).", "MEDIUM"),
        # Q17
        ("Find the wrong number in the series: 1, 2, 3, 5, 8, 14, 21",
         ["3", "5", "14", "21"], 2,
         "Each term should be the sum of the two before it: 1, 2, 3, 5, 8, 13, 21. The term 14 breaks the pattern (should be 5 + 8 = 13). Key Learning Point: Test the Fibonacci rule at every step – the first sum that fails identifies the wrong term.", "MEDIUM"),
        # Q18
        ("Find the next term: 3, 9, 10, 30, 31, 93, ?",
         ["94", "95", "186", "279"], 0,
         "Alternating operations: ×3, +1, repeating. 3×3=9, 9+1=10, 10×3=30, 30+1=31, 31×3=93, 93+1=94. Key Learning Point: Identify which operation of the alternating pair comes next before calculating.", "MEDIUM"),
        # Q19
        ("Find the next term: 2, 8, 32, 128, ?",
         ["256", "384", "512", "640"], 2,
         "Constant ratio ×4. 128 × 4 = 512. Key Learning Point: If ×2 and ×3 do not fit, test other ratios such as ×4.", "EASY"),
        # Q20
        ("Find the next term: 720, 360, 120, 30, 6, ?",
         ["0", "1", "2", "3"], 1,
         "The divisors increase by 1: ÷2, ÷3, ÷4, ÷5, ÷6. 6 ÷ 6 = 1. Key Learning Point: A decreasing series may divide by a changing number – write the ratios as a row to see the pattern.", "EASY"),
        # Q21
        ("Find the next term: 1, 3, 8, 19, 42, ?",
         ["84", "86", "89", "91"], 2,
         "×2 plus an increasing number: 1×2+1=3, 3×2+2=8, 8×2+3=19, 19×2+4=42, 42×2+5=89. Key Learning Point: In a “×2 + constant” series, check whether the added number is fixed or itself increasing.", "MEDIUM"),
        # Q22
        ("Find the wrong number in the series: 4, 7, 12, 20, 28, 39",
         ["7", "12", "20", "28"], 2,
         "Pattern: n² + 3 → 4, 7, 12, 19, 28, 39. The term 20 breaks the pattern (should be 19). Key Learning Point: Compute the formula-based value for every position before deciding which term is wrong.", "MEDIUM"),
        # Q23
        ("Find the next term: 2, 3, 5, 8, 13, 21, ?",
         ["29", "31", "33", "34"], 3,
         "Each term is the sum of the two preceding terms. 13 + 21 = 34. Key Learning Point: Extend a Fibonacci-type series by adding the last two terms.", "EASY"),
        # Q24
        ("Find the missing term: 2, 12, 36, ?, 150",
         ["64", "72", "80", "96"], 2,
         "Pattern: n² × (n + 1): 1×2=2, 4×3=12, 9×4=36, 16×5=80, 25×6=150. Key Learning Point: Check the missing term against the next term – n = 5 gives 150, confirming 80.", "MEDIUM"),
        # Q25
        ("Find the next term: 2, 10, 50, 250, ?",
         ["1000", "1250", "1500", "1750"], 1,
         "Constant ratio ×5. 250 × 5 = 1250. Key Learning Point: Confirm the ratio with every consecutive pair before extending the series.", "EASY"),
        # Q26
        ("Find the missing term: 8, 15, 12, 19, 16, 23, 20, ?",
         ["24", "25", "26", "27"], 3,
         "Alternating operations: +7, −3, repeating. 20 + 7 = 27 (Also: odd positions 8, 12, 16, 20 and even positions 15, 19, 23, 27 each increase by 4). Key Learning Point: Split the series into odd and even positions when the alternating steps are not obvious.", "MEDIUM"),
        # Q27
        ("Find the missing term: 5, 6, 10, 19, ?, 60",
         ["29", "32", "35", "38"], 2,
         "The differences are perfect squares: 1, 4, 9, 16, 25. 19 + 16 = 35, and 35 + 25 = 60 confirms the answer. Key Learning Point: Differences can themselves form a familiar series (here, squares) – write them out as a separate row.", "MEDIUM"),
        # Q28
        ("Find the next term: 1, 2, 6, 6, 11, 18, 16, ?",
         ["21", "36", "48", "54"], 3,
         "Odd positions: 1, 6, 11, 16 (+5 each). Even positions: 2, 6, 18, ? (×3 each) → 54. Key Learning Point: Split the series by position and find a separate rule for each sub-series.", "MEDIUM"),
        # Q29
        ("Find the next term: 1, 4, 27, 256, ?",
         ["625", "1024", "3125", "4096"], 2,
         "Each term is n raised to the power n: 1¹, 2², 3³, 4⁴, 5⁵ = 3125. Key Learning Point: Rapidly growing series may use powers such as nⁿ – test this when squares and cubes do not fit.", "MEDIUM"),
        # Q30
        ("Find the wrong number in the series: 5, 10, 8, 13, 11, 17, 14",
         ["10", "13", "14", "17"], 3,
         "Alternating operations: +5, −2 → 5, 10, 8, 13, 11, 16, 14. The term 17 breaks the pattern (should be 16). Key Learning Point: In an alternating series, a wrong term makes both of its neighbouring steps look wrong – find the single change that restores the pattern.", "MEDIUM")
    ]

    # 30 Assessment Questions (Tamil)
    assess_ta = [
        # Q1
        ("அடுத்த உறுப்பைக் காண்க: 8, 16, 24, 32, ?",
         ["36", "38", "40", "42"], 2,
         "மாறா வித்தியாசம் +8. 32 + 8 = 40. முக்கியக் கற்றல் கருத்து: முதலில் மாறா வித்தியாசத்தைச் சரிபார்க்கவும்."),
        # Q2
        ("அடுத்த உறுப்பைக் காண்க: 2, 3, 6, 11, 18, ?",
         ["25", "27", "29", "31"], 1,
         "வித்தியாசங்கள்: 1, 3, 5, 7 (அடுத்தடுத்த ஒற்றை எண்கள்). அடுத்த வித்தியாசம் = 9: 18 + 9 = 27. முக்கியக் கற்றல் கருத்து: வித்தியாசம் மாறாமல் இல்லாதபோது, வித்தியாசங்களே ஓர் எளிய தொடரை அமைக்கின்றனவா எனச் சரிபார்க்கவும்."),
        # Q3
        ("அடுத்த உறுப்பைக் காண்க: 50, 45, 41, 38, 36, ?",
         ["33", "34", "35", "36"], 2,
         "வித்தியாசங்கள்: −5, −4, −3, −2. அடுத்த வித்தியாசம் = −1: 36 − 1 = 35. முக்கியக் கற்றல் கருத்து: குறையும் தொடரில் இடைவெளி சீராகச் சுருங்கலாம் – அதைக் காண வித்தியாசங்களை எழுதவும்."),
        # Q4
        ("அடுத்த உறுப்பைக் காண்க: 80, 70, 60, 50, ?",
         ["35", "38", "40", "42"], 2,
         "மாறா வித்தியாசம் −10. 50 − 10 = 40. முக்கியக் கற்றல் கருத்து: குறையும் கூட்டுத் தொடருக்கு எதிர்மறை மாறா வித்தியாசம் உண்டு."),
        # Q5
        ("அடுத்த உறுப்பைக் காண்க: 1, 2, 4, 8, 15, 26, ?",
         ["40", "42", "44", "46"], 1,
         "முதல்நிலை வித்தியாசங்கள்: 1, 2, 4, 7, 11. இரண்டாம்நிலை வித்தியாசங்கள்: 1, 2, 3, 4 → அடுத்தது = 5; எனவே அடுத்த முதல்நிலை வித்தியாசம் = 16. 26 + 16 = 42. முக்கியக் கற்றல் கருத்து: முதல்நிலை வித்தியாசங்கள் ஒழுங்காக இல்லையெனில், மீண்டும் வித்தியாசம் காணவும் – இரண்டாம்நிலை அமைப்பு பெரும்பாலும் வெளிப்படும்."),
        # Q6
        ("அடுத்த உறுப்பைக் காண்க: 1, 2, 6, 12, 36, 72, ?",
         ["144", "180", "216", "288"], 2,
         "மாறி மாறி வரும் பெருக்கல்: ×2, ×3, மீண்டும் மீண்டும். 72 × 3 = 216. முக்கியக் கற்றல் கருத்து: பெருக்குத் தொடர் வகை இரண்டு வெவ்வேறு பெருக்கிகளுக்கிடையே மாறி மாறி வரலாம்."),
        # Q7
        ("அடுத்த உறுப்பைக் காண்க: 5, 9, 17, 33, 65, ?",
         ["125", "127", "129", "131"], 2,
         "அமைப்பு: ஒவ்வொரு முறையும் ×2 − 1. 5×2−1=9, 9×2−1=17, 17×2−1=33, 33×2−1=65, 65×2−1=129. முக்கியக் கற்றல் கருத்து: தொடரை நீட்டிக்கும் முன், “×மாறிலி − மாறிலி” அமைப்பை ஒவ்வோர் உறுப்புடனும் சரிபார்க்கவும்."),
        # Q8
        ("அடுத்த உறுப்பைக் காண்க: 1, 3, 6, 10, 15, ?",
         ["18", "20", "21", "25"], 2,
         "வித்தியாசங்கள்: 2, 3, 4, 5, 6. 15 + 6 = 21 (இவை முக்கோண எண்கள்). முக்கியக் கற்றல் கருத்து: 1 அதிகரிக்கும் வித்தியாசங்கள் 1, 3, 6, 10, 15, 21… என்ற முக்கோண எண்களைத் தருகின்றன."),
        # Q9
        ("அடுத்த உறுப்பைக் காண்க: 3, 10, 21, 36, 55, ?",
         ["74", "76", "78", "80"], 2,
         "வித்தியாசங்கள்: 7, 11, 15, 19 (4 அதிகரிக்கிறது). அடுத்த வித்தியாசம் = 23: 55 + 23 = 78. முக்கியக் கற்றல் கருத்து: வித்தியாசங்களே ஒரு கூட்டுத் தொடரை அமைக்கும்போது, அடுத்த வித்தியாசத்தைக் காண அத்தொடரைத் தொடரவும்."),
        # Q10
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 1, 8, 27, 65, 125, 216",
         ["8", "27", "65", "125"], 2,
         "கனங்கள்: 1³, 2³, 3³, 4³, 5³, 6³ = 1, 8, 27, 64, 125, 216. 65 என்ற உறுப்பு அமைப்பை உடைக்கிறது (64 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: கன அமைப்பு அடையாளம் காணப்பட்டதும், எதிர்பார்க்கப்படும் ஒவ்வொரு கனத்தையும் கணக்கிடவும் – ஒன்று கூடுதலாகவோ குறைவாகவோ உள்ள உறுப்பே பொறி."),
        # Q11
        ("அடுத்த உறுப்பைக் காண்க: 3, 4, 7, 11, 18, 29, ?",
         ["44", "45", "46", "47"], 3,
         "ஒவ்வோர் உறுப்பும் முந்தைய இரண்டு உறுப்புகளின் கூடுதல்: 3+4=7, 4+7=11, 7+11=18, 11+18=29, 18+29=47. முக்கியக் கற்றல் கருத்து: ஃபிபோனச்சி வகைத் தொடர் எந்த இரண்டு எண்களிலிருந்தும் தொடங்கலாம்."),
        # Q12
        ("அடுத்த உறுப்பைக் காண்க: 4, 6, 10, 14, 22, 26, ?",
         ["30", "32", "34", "38"], 2,
         "ஒவ்வோர் உறுப்பும் ஒரு பகா எண்ணின் இருமடங்கு: 2×2, 2×3, 2×5, 2×7, 2×11, 2×13. அடுத்த பகா எண் 17; எனவே அடுத்த உறுப்பு = 2 × 17 = 34. முக்கியக் கற்றல் கருத்து: உறுப்புகள் அனைத்தும் இரட்டை எண்களாகவும் இடைவெளிகள் ஒழுங்கற்றதாகவும் இருந்தால், அவற்றைப்பாதியாக்கவும் – ஒரு பழக்கமான தொடர் (இங்கு, பகா எண்கள்) வெளிப்படலாம்."),
        # Q13
        ("அடுத்த உறுப்பைக் காண்க: 1, 8, 9, 64, 25, 216, ?",
         ["36", "49", "343", "512"], 1,
         "ஒற்றை இடங்கள் வர்க்கங்கள்; இரட்டை இடங்கள் கனங்கள்: 1², 2³, 3², 4³, 5², 6³. 7-ஆவது உறுப்பு ஒரு வர்க்கம்: 7² = 49. முக்கியக் கற்றல் கருத்து: வர்க்கங்களும் கனங்களும் சேர்ந்து வரும்போது, அவை இடத்தின்படி மாறி மாறி வருகின்றனவா எனச் சரிபார்க்கவும்."),
        # Q14
        ("அடுத்த உறுப்பைக் காண்க: 0, 6, 24, 60, 120, ?",
         ["180", "200", "210", "216"], 2,
         "அமைப்பு: n³ − n → 1−1, 8−2, 27−3, 64−4, 125−5, 216−6 = 210. (இதற்குச் சமமாக, அடுத்தடுத்த மூன்று எண்களின் பெருக்கற்பலன்: 5 × 6 × 7 = 210.) முக்கியக் கற்றல் கருத்து: முழுக் கனங்களைவிடச் சற்று குறைவான எண்கள் n³ − n போன்ற கன அடிப்படை மாறுபாட்டைக் குறிக்கின்றன."),
        # Q15
        ("அடுத்த உறுப்பைக் காண்க: 1, 4, 8, 11, 22, 25, ?",
         ["28", "48", "50", "75"], 2,
         "மாறி மாறி வரும் செயல்கள்: +3, ×2, மீண்டும் மீண்டும். 1+3=4, 4×2=8, 8+3=11, 11×2=22, 22+3=25, 25×2=50. முக்கியக் கற்றல் கருத்து: மீண்டும் வரும் இணையின் இரு செயல்களையும் கண்டறிந்து, அடுத்த படியில் எது பொருந்துகிறது எனப் பின்தொடரவும்."),
        # Q16
        ("விடுபட்ட உறுப்பைக் காண்க: 3, 5, 7, 10, 11, 20, 15, ?",
         ["25", "30", "35", "40"], 3,
         "ஒற்றை இடங்கள்: 3, 7, 11, 15 (ஒவ்வொன்றும் +4). இரட்டை இடங்கள்: 5, 10, 20, ? (ஒவ்வொன்றும் ×2) → 40. முக்கியக் கற்றல் கருத்து: இடையிட்ட தொடரின் இரு உட்தொடர்களும் வெவ்வேறு செயல்களைப் (இங்கு, +4 மற்றும் ×2) பின்பற்றலாம்."),
        # Q17
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 1, 2, 3, 5, 8, 14, 21",
         ["3", "5", "14", "21"], 2,
         "ஒவ்வோர் உறுப்பும் அதற்கு முந்தைய இரண்டின் கூடுதலாக இருக்க வேண்டும்: 1, 2, 3, 5, 8, 13, 21. 14 என்ற உறுப்பு அமைப்பை உடைக்கிறது (5 + 8 = 13 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: ஒவ்வொரு படியிலும் ஃபிபோனச்சி விதியைச் சோதிக்கவும் – தோல்வியடையும் முதல் கூடுதலே தவறான உறுப்பைக் காட்டுகிறது."),
        # Q18
        ("அடுத்த உறுப்பைக் காண்க: 3, 9, 10, 30, 31, 93, ?",
         ["94", "95", "186", "279"], 0,
         "மாறி மாறி வரும் செயல்கள்: ×3, +1, மீண்டும் மீண்டும். 3×3=9, 9+1=10, 10×3=30, 30+1=31, 31×3=93, 93+1=94. முக்கியக் கற்றல் கருத்து: கணக்கிடும் முன், மாறி மாறி வரும் இணையின் எந்தச் செயல் அடுத்து வருகிறது எனக் கண்டறியவும்."),
        # Q19
        ("அடுத்த உறுப்பைக் காண்க: 2, 8, 32, 128, ?",
         ["256", "384", "512", "640"], 2,
         "மாறா விகிதம் ×4. 128 × 4 = 512. முக்கியக் கற்றல் கருத்து: ×2, ×3 பொருந்தவில்லையெனில், ×4 போன்ற பிற விகிதங்களைச் சோதிக்கவும்."),
        # Q20
        ("அடுத்த உறுப்பைக் காண்க: 720, 360, 120, 30, 6, ?",
         ["0", "1", "2", "3"], 1,
         "வகுஎண்கள் 1 அதிகரிக்கின்றன: ÷2, ÷3, ÷4, ÷5, ÷6. 6 ÷ 6 = 1. முக்கியக் கற்றல் கருத்து: குறையும் தொடர் மாறும் எண்ணால் வகுக்கலாம் – அமைப்பைக் காண விகிதங்களை வரிசையாக எழுதவும்."),
        # Q21
        ("அடுத்த உறுப்பைக் காண்க: 1, 3, 8, 19, 42, ?",
         ["84", "86", "89", "91"], 2,
         "×2 கூட்டல் அதிகரிக்கும் எண்: 1×2+1=3, 3×2+2=8, 8×2+3=19, 19×2+4=42, 42×2+5=89. முக்கியக் கற்றல் கருத்து: “×2 + மாறிலி” தொடரில், கூட்டப்படும் எண் நிலையானதா அல்லது அதுவே அதிகரிக்கிறதா எனச் சரிபார்க்கவும்."),
        # Q22
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 4, 7, 12, 20, 28, 39",
         ["7", "12", "20", "28"], 2,
         "அமைப்பு: n² + 3 → 4, 7, 12, 19, 28, 39. 20 என்ற உறுப்பு அமைப்பை உடைக்கிறது (19 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: எந்த உறுப்பு தவறு என முடிவு செய்யும் முன், ஒவ்வோர் இடத்துக்குமான சூத்திர அடிப்படையிலான மதிப்பைக் கணக்கிடவும்."),
        # Q23
        ("அடுத்த உறுப்பைக் காண்க: 2, 3, 5, 8, 13, 21, ?",
         ["29", "31", "33", "34"], 3,
         "ஒவ்வோர் உறுப்பும் முந்தைய இரண்டு உறுப்புகளின் கூடுதல். 13 + 21 = 34. முக்கியக் கற்றல் கருத்து: கடைசி இரண்டு உறுப்புகளைக் கூட்டி ஃபிபோனச்சி வகைத் தொடரை நீட்டிக்கவும்."),
        # Q24
        ("விடுபட்ட உறுப்பைக் காண்க: 2, 12, 36, ?, 150",
         ["64", "72", "80", "96"], 2,
         "அமைப்பு: n² × (n + 1): 1×2=2, 4×3=12, 9×4=36, 16×5=80, 25×6=150. முக்கியக் கற்றல் கருத்து: விடுபட்ட உறுப்பை அடுத்த உறுப்புடன் சரிபார்க்கவும் – n = 5 எனில் 150 கிடைக்கிறது; இது 80 என்பதை உறுதிசெய்கிறது."),
        # Q25
        ("அடுத்த உறுப்பைக் காண்க: 2, 10, 50, 250, ?",
         ["1000", "1250", "1500", "1750"], 1,
         "மாறா விகிதம் ×5. 250 × 5 = 1250. முக்கியக் கற்றல் கருத்து: தொடரை நீட்டிக்கும் முன், அடுத்தடுத்த ஒவ்வோர் இணையுடனும் விகிதத்தை உறுதிசெய்யவும்."),
        # Q26
        ("விடுபட்ட உறுப்பைக் காண்க: 8, 15, 12, 19, 16, 23, 20, ?",
         ["24", "25", "26", "27"], 3,
         "மாறி மாறி வரும் செயல்கள்: +7, −3, மீண்டும் மீண்டும். 20 + 7 = 27 (மேலும்: ஒற்றை இடங்கள் 8, 12, 16, 20 மற்றும் இரட்டை இடங்கள் 15, 19, 23, 27 ஒவ்வொன்றும் 4 அதிகரிக்கின்றன). முக்கியக் கற்றல் கருத்து: மாறி மாறி வரும் படிகள் வெளிப்படையாகத் தெரியாதபோது, தொடரை ஒற்றை மற்றும் இரட்டை இடங்களாகப் பிரிக்கவும்."),
        # Q27
        ("விடுபட்ட உறுப்பைக் காண்க: 5, 6, 10, 19, ?, 60",
         ["29", "32", "35", "38"], 2,
         "வித்தியாசங்கள் முழு வர்க்கங்கள்: 1, 4, 9, 16, 25. 19 + 16 = 35; மேலும் 35 + 25 = 60 என்பது விடையை உறுதிசெய்கிறது. முக்கியக் கற்றல் கருத்து: வித்தியாசங்களே ஒரு பழக்கமான தொடரை (இங்கு, வர்க்கங்கள்) அமைக்கலாம் – அவற்றைத்தனி வரிசையாக எழுதவும்."),
        # Q28
        ("அடுத்த உறுப்பைக் காண்க: 1, 2, 6, 6, 11, 18, 16, ?",
         ["21", "36", "48", "54"], 3,
         "ஒற்றை இடங்கள்: 1, 6, 11, 16 (ஒவ்வொன்றும் +5). இரட்டை இடங்கள்: 2, 6, 18, ? (ஒவ்வொன்றும் ×3) → 54. முக்கியக் கற்றல் கருத்து: தொடரை இடத்தின்படி பிரித்து, ஒவ்வோர் உட்தொடருக்கும் தனி விதியைக் காணவும்."),
        # Q29
        ("அடுத்த உறுப்பைக் காண்க: 1, 4, 27, 256, ?",
         ["625", "3125", "1024", "4096"], 1,
         "ஒவ்வோர் உறுப்பும் n-இன் n-ஆம் அடுக்கு: 1¹, 2², 3³, 4⁴, 5⁵ = 3125. முக்கியக் கற்றல் கருத்து: வேகமாக வளரும் தொடர்கள் nⁿ போன்ற அடுக்குகளைப் பயன்படுத்தலாம் – வர்க்கங்களும் கனங்களும் பொருந்தாதபோது இதைச் சோதிக்கவும்."),
        # Q30
        ("தொடரில் உள்ள தவறான எண்ணைக் காண்க: 5, 10, 8, 13, 11, 17, 14",
         ["10", "13", "14", "17"], 3,
         "மாறி மாறி வரும் செயல்கள்: +5, −2 → 5, 10, 8, 13, 11, 16, 14. 17 என்ற உறுப்பு அமைப்பை உடைக்கிறது (16 ஆக இருக்க வேண்டும்). முக்கியக் கற்றல் கருத்து: மாறி மாறி வரும் தொடரில், ஒரு தவறான உறுப்பு அதன் இருபுறப் படிகளையும் தவறாகக் காட்டும் – அமைப்பை மீட்டெடுக்கும் ஒற்றை மாற்றத்தைக் கண்டறியவும்.")
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
    out_lines.append("   ExamPro LMS - Number Series Course Seed Script (Unified Bilingual Model)")
    out_lines.append("   - 1 Course: Number Series / எண் தொடர்கள்")
    out_lines.append("   - 2 Assessments (Single unified assessment for both English & Tamil):")
    out_lines.append("       1. Number Series - Practice Set (number-series-practice) [55 Questions]")
    out_lines.append("          (25 Worked Examples + 30 Independent Practice in both English & Tamil)")
    out_lines.append("       2. Number Series - Graded Assessment (number-series-graded) [30 Questions]")
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
    out_lines.append("-- Clean previous Number Series courses and assessments if present")
    out_lines.append("DELETE FROM dbo.Assessments WHERE Slug IN (")
    out_lines.append("    N'number-series-practice', N'number-series-graded',")
    out_lines.append("    N'number-series-practice-en', N'number-series-graded-en',")
    out_lines.append("    N'number-series-practice-ta', N'number-series-graded-ta'")
    out_lines.append(");")
    out_lines.append("DELETE FROM dbo.Courses WHERE Slug IN (N'number-series');")
    out_lines.append("")
    out_lines.append("INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)")
    out_lines.append("VALUES (")
    out_lines.append("    N'Number Series / எண் தொடர்கள்',")
    out_lines.append("    N'number-series',")
    out_lines.append("    N'Comprehensive module on Arithmetic, Geometric, Square, Cube, Prime, Fibonacci, Alternating-Operation, and Two-Interleaved Series for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',")
    out_lines.append("    6")
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
    out_lines.append("    (@CourseId, N'Number Series - Practice Set', N'எண் தொடர்கள் - பயிற்சித் தொகுப்பு', N'number-series-practice',")
    out_lines.append("     N'55 practice questions (Worked Examples + Independent Practice) with instant feedback & step-by-step solutions.',")
    out_lines.append("     N'55 பயிற்சிக் கணக்குகள் (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனடித் தீர்வுகளுடன்.',")
    out_lines.append("     N'Number Series', N'EASY', 60, 10, 55, 0, N'PRACTICE', 0, 0, 0, 1),")
    out_lines.append("    (@CourseId, N'Number Series - Graded Assessment', N'எண் தொடர்கள் - மதிப்பீட்டுத் தேர்வு', N'number-series-graded',")
    out_lines.append("     N'Official proctored & timed assessment on Number Series (30 Questions). Pass with 60% to master this topic.',")
    out_lines.append("     N'எண் தொடர்களுக்கான அதிகாரப்பூர்வக் கண்காணிப்புடன் கூடிய தேர்வு (30 வினாக்கள்). தேர்ச்சி 60%.',")
    out_lines.append("     N'Number Series', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 2);")
    out_lines.append("")
    out_lines.append("DECLARE @pracId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'number-series-practice');")
    out_lines.append("DECLARE @gradId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'number-series-graded');")
    out_lines.append("")
    out_lines.append("-- Insert bilingual questions for @pracId (55 questions)")
    out_lines.append("INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, QuestionTextTa, OptionsJsonTa, ExplanationTa, Topic, Difficulty, OrderIndex)")
    out_lines.append("VALUES")

    p_rows = []
    for idx, (en, ta) in enumerate(zip(prac_en, prac_ta), start=1):
        q_en, opts_en, ans_en, exp_en, diff_en = en
        q_ta, opts_ta, ans_ta, exp_ta = ta
        p_rows.append(f"    (@pracId, {escape_sql(q_en)}, {escape_sql(json.dumps(opts_en, ensure_ascii=False))}, {ans_en}, {escape_sql(exp_en)}, {escape_sql(q_ta)}, {escape_sql(json.dumps(opts_ta, ensure_ascii=False))}, {escape_sql(exp_ta)}, N'Number Series', N'{diff_en}', {idx})")

    out_lines.append(",\n".join(p_rows) + ";")
    out_lines.append("")

    out_lines.append("-- Insert bilingual questions for @gradId (30 questions)")
    out_lines.append("INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, QuestionTextTa, OptionsJsonTa, ExplanationTa, Topic, Difficulty, OrderIndex)")
    out_lines.append("VALUES")

    g_rows = []
    for idx, (en, ta) in enumerate(zip(assess_en, assess_ta), start=1):
        q_en, opts_en, ans_en, exp_en, diff_en = en
        q_ta, opts_ta, ans_ta, exp_ta = ta
        g_rows.append(f"    (@gradId, {escape_sql(q_en)}, {escape_sql(json.dumps(opts_en, ensure_ascii=False))}, {ans_en}, {escape_sql(exp_en)}, {escape_sql(q_ta)}, {escape_sql(json.dumps(opts_ta, ensure_ascii=False))}, {escape_sql(exp_ta)}, N'Number Series', N'{diff_en}', {idx})")

    out_lines.append(",\n".join(g_rows) + ";")
    out_lines.append("")
    out_lines.append("COMMIT;")
    out_lines.append("PRINT 'Number Series Course seeded successfully: 1 Practice Assessment (55 Qs) and 1 Graded Assessment (30 Qs), fully bilingual (English & Tamil).';")
    out_lines.append("GO")

    out_path = os.path.join(os.path.dirname(__file__), "09_number_series_bilingual_seed.sql")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Generated {out_path} ({len(out_lines)} lines)")

if __name__ == '__main__':
    main()
