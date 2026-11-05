# -*- coding: utf-8 -*-
"""Generates 04_percentage_bilingual_seed.sql containing all 180 questions from English and Tamil Percentage PDFs."""
import json
import os

def escape_sql(text: str) -> str:
    if text is None:
        return 'NULL'
    return "N'" + text.replace("'", "''") + "'"

def main():
    # 30 Worked Examples (English)
    worked_en = [
        ("The value of an investment increases from ₹75,000 to ₹84,000. Find the percentage increase.", ["10%", "11%", "12%", "15%"], 2, "Increase = ₹84,000 − ₹75,000 = ₹9,000. Percentage Increase = (9,000 / 75,000) × 100 = 12%. Key Learning Point: Percentage increase = (Increase in value ÷ Original value) × 100.", "EASY"),
        ("In a college, 40% of students are girls. If the number of boys increases by 25%, while the number of girls remains unchanged, what percentage of the total students are girls now?", ["32%", "34.8%", "36%", "38%"], 1, "Assume Total = 100. Girls = 40, Boys = 60. New Boys = 60 × 1.25 = 75. New Total = 115. Girls % = (40 / 115) × 100 = 34.8%. Key Learning Point: When one group changes, recalculate total before finding new %.", "MEDIUM"),
        ("30 liters of a solution with 20% acid concentration is mixed with 20 litres of a solution with 40% acid concentration. Find the acid concentration of the resulting mixture.", ["24%", "26%", "28%", "30%"], 2, "Total acid = (30 × 20%) + (20 × 40%) = 6 + 8 = 14 L. Total mixture = 50 L. Concentration = (14 / 50) × 100 = 28%. Key Learning Point: Find actual quantity of component in each part first, then divide by combined total.", "MEDIUM"),
        ("The price of a commodity is first reduced by 20% and later increased by 25%. Compared to the original price, the final price is:", ["2% increase", "4% increase", "No change", "5% decrease"], 2, "Assume 100. After -20% = 80. After +25% = 80 × 1.25 = 100. Multiplier = 0.80 × 1.25 = 1.00 (No change). Key Learning Point: Successive changes must be verified using multiplier chain.", "EASY"),
        ("The price of an article increases by 12%. By what percentage should consumption be reduced so that expenditure remains unchanged?", ["10%", "10.71%", "12%", "12.5%"], 1, "Reduction = [r / (100 + r)] × 100 = (12 / 112) × 100 = 10.71%. Key Learning Point: For expenditure-constant problems, use: [r / (100 + r)] × 100.", "MEDIUM"),
        ("The population of a village is 15,000. If it increases by 12%, what will be the new population?", ["16,500", "16,700", "16,800", "17,000"], 2, "New population = 15,000 × 1.12 = 16,800. Key Learning Point: For single percentage increase, multiply original by (100 + rate)/100.", "EASY"),
        ("A trader buys two articles of the same cost price. He sells one at a 40% profit and the other at a 10% loss. Find his overall percentage profit or loss.", ["10% profit", "15% profit", "10% loss", "15% loss"], 1, "Total CP = 2x. Total SP = 1.40x + 0.90x = 2.30x. Overall profit % = (0.30 / 2) × 100 = 15% profit. Key Learning Point: For equal CP, net % = (profit% - loss%) / 2.", "EASY"),
        ("A trader buys two articles of the same cost price. He sells one at a 30% profit and the other at a 10% loss. Find his overall percentage profit or loss.", ["5% profit", "10% profit", "5% loss", "10% loss"], 1, "Total CP = 2x. Total SP = 1.30x + 0.90x = 2.20x. Overall profit % = (0.20 / 2) × 100 = 10% profit.", "EASY"),
        ("A trader buys two articles of the same cost price. He sells one at a 25% profit and the other at a 15% loss. Find his overall percentage profit or loss.", ["5% profit", "5% loss", "10% profit", "10% loss"], 0, "Total CP = 2x. Total SP = 1.25x + 0.85x = 2.10x. Overall profit % = (0.10 / 2) × 100 = 5% profit.", "EASY"),
        ("The price of an article is increased by 25% and later decreased by 20%. Compared to the original price, the final price is:", ["5% increase", "5% decrease", "No change", "4% decrease"], 2, "100 × 1.25 × 0.80 = 100. No change. Key Learning Point: 1.25 × 0.80 = 1.00.", "EASY"),
        ("The expenditure of a family increases by 20%, while its income increases by 10%. If the family was saving ₹6,000 earlier out of an income of ₹30,000, what is the new saving?", ["₹3,600", "₹4,200", "₹4,800", "₹5,400"], 1, "Original Exp = 30,000 - 6,000 = 24,000. New Income = 30,000 × 1.10 = 33,000. New Exp = 24,000 × 1.20 = 28,800. New Saving = 33,000 - 28,800 = ₹4,200.", "MEDIUM"),
        ("Out of a fixed voter base of 60,000, a candidate's vote share increased from 25% to 31% between two elections. Find the percentage increase in the actual number of votes received.", ["20%", "22%", "24%", "26%"], 2, "Votes earlier = 25% of 60,000 = 15,000. Votes now = 31% of 60,000 = 18,600. Increase = 3,600. % increase = (3,600 / 15,000) × 100 = 24%.", "MEDIUM"),
        ("A candidate secured 480 marks and failed by 8% of the maximum marks. If the pass mark is 68%, what is the maximum mark?", ["720", "750", "800", "840"], 2, "Pass % = 68%. Candidate % = 68% - 8% = 60%. 60% = 480 marks. Max Marks = (480 × 100) / 60 = 800.", "MEDIUM"),
        ("The price of sugar is reduced by 25%. By what percentage should consumption increase to keep expenditure unchanged?", ["20%", "25%", "30%", "33⅓%"], 3, "Required Increase = [r / (100 - r)] × 100 = (25 / 75) × 100 = 33⅓%.", "MEDIUM"),
        ("The population of a town increases by 10% in the first year, 20% in the second year and decreases by 10% in the third year. What is the overall percentage change?", ["18.8% increase", "20% increase", "21% increase", "22% increase"], 0, "100 × 1.10 × 1.20 × 0.90 = 118.8 → 18.8% increase.", "MEDIUM"),
        ("The value of a machine depreciates by 10% every year. If its current value is ₹72,900, what was its value one year ago?", ["₹79,000", "₹80,000", "₹81,000", "₹82,000"], 2, "Original Value = 72,900 ÷ 0.90 = ₹81,000.", "EASY"),
        ("The value of a machine depreciates by 20%. If its present value is ₹48,000, find its value before depreciation.", ["₹58,000", "₹60,000", "₹62,000", "₹64,000"], 1, "Original = 48,000 ÷ 0.80 = ₹60,000.", "EASY"),
        ("The value of a machine depreciates by 10% every year. If its present value (after 3 years of depreciation) is ₹2,50,047, find its original value.", ["₹3,23,000", "₹3,33,000", "₹3,43,000", "₹3,53,000"], 2, "Original = 2,50,047 ÷ (0.90)³ = 2,50,047 ÷ 0.729 = ₹3,43,000.", "HARD"),
        ("The value of a machine depreciates by 10% every year. If its present value (after 2 years of depreciation) is ₹1,94,481, find its original value.", ["₹2,20,100", "₹2,30,100", "₹2,40,100", "₹2,50,100"], 2, "Original = 1,94,481 ÷ (0.90)² = 1,94,481 ÷ 0.81 = ₹2,40,100.", "HARD"),
        ("The income of a person is increased by 20% and his expenditure is increased by 15%. Initially, he saved 20% of his income. By what percentage does his saving increase?", ["20%", "30%", "40%", "50%"], 2, "Assume Income = 100, Saving = 20, Exp = 80. New Income = 120, New Exp = 80 × 1.15 = 92. New Saving = 120 - 92 = 28. % Increase in saving = ((28 - 20)/20) × 100 = 40%.", "MEDIUM"),
        ("In an examination, 84% of the candidates passed. If 1,260 candidates passed, how many candidates appeared for the examination?", ["1,400", "1,450", "1,500", "1,550"], 2, "Total = (1,260 × 100) / 84 = 1,500.", "EASY"),
        ("40 litres of a solution with 15% salt concentration is mixed with 10 litres of a solution with 35% salt concentration. Find the salt concentration of the resulting mixture.", ["17%", "19%", "21%", "23%"], 1, "Salt = (40 × 15%) + (10 × 35%) = 6 + 3.5 = 9.5 L. Total mixture = 50 L. Concentration = (9.5 / 50) × 100 = 19%.", "MEDIUM"),
        ("Out of a fixed voter base of 80,000, a candidate's vote share increased from 35% to 42% between two elections. Find the percentage increase in the actual number of votes received.", ["15%", "18%", "20%", "22%"], 2, "Votes earlier = 35% of 80,000 = 28,000. Votes now = 42% of 80,000 = 33,600. Increase = 5,600. % increase = (5,600 / 28,000) × 100 = 20%.", "MEDIUM"),
        ("A candidate secures 45% marks and fails by 30 marks. Another candidate secures 60% marks and obtains 60 marks more than the pass mark. The maximum marks are:", ["500", "600", "700", "800"], 1, "Difference in % = 60% - 45% = 15%. Difference in marks = 30 + 60 = 90. Max Marks = (90 × 100) / 15 = 600.", "MEDIUM"),
        ("In a competitive examination, 35% candidates failed in Mathematics, 25% failed in English and 15% failed in both subjects. If 550 candidates passed in both subjects, find the total number of candidates.", ["900", "960", "1,000", "None of the above"], 2, "Failed in at least one = 35 + 25 - 15 = 45%. Passed in both = 100 - 45 = 55%. 55% = 550 → Total = (550 × 100) / 55 = 1,000.", "HARD"),
        ("A's income is 150% more than B's income. By what percentage is B's income less than A's income?", ["40%", "50%", "60%", "70%"], 2, "Let B = 100 → A = 250. B is less than A by 150. % = (150 / 250) × 100 = 60%.", "MEDIUM"),
        ("In an examination, 40% of the candidates failed in Mathematics, 30% failed in English, and 15% failed in both subjects. What percentage of candidates passed in both subjects?", ["40%", "45%", "50%", "55%"], 1, "Failed at least one = 40 + 30 - 15 = 55%. Passed in both = 100 - 55 = 45%.", "MEDIUM"),
        ("A number is decreased by 15% and then increased by 25%. Find the overall percentage change.", ["4.25% increase", "6.25% increase", "8.25% increase", "10.25% increase"], 1, "Multiplier = 0.85 × 1.25 = 1.0625 → 6.25% increase.", "EASY"),
        ("A school has 1,500 students. 48% are girls. If the number of boys increases by 20% while the number of girls remains the same, what is the new percentage of girls?", ["42.3%", "43.5%", "44.6%", "45.8%"], 1, "Girls = 720, Boys = 780. New Boys = 780 × 1.20 = 936. New Total = 720 + 936 = 1656. Girls % = (720 / 1656) × 100 ≈ 43.5%.", "MEDIUM"),
        ("A number is increased by 40% and then decreased by 25%. The final value is:", ["5% less than original", "Equal to original", "5% greater than original", "10% greater than original"], 2, "100 × 1.40 × 0.75 = 105 → 5% greater than original.", "EASY")
    ]

    # 30 Independent Practice (English)
    indep_en = [
        ("The population of a town increased by 10% in the first year and then decreased by 8% in the second year, resulting in a final population of 20,240. Find the original population.", ["19,500", "19,800", "20,000", "20,200"], 2, "Multiplier = 1.10 × 0.92 = 1.012. Original = 20,240 ÷ 1.012 = 20,000.", "MEDIUM"),
        ("The price of an article is increased by 20% and later decreased by 10%. The overall percentage change is:", ["8% increase", "10% increase", "12% increase", "2% increase"], 0, "100 × 1.20 × 0.90 = 108 → 8% increase.", "EASY"),
        ("The value of a machine depreciates by 20% every year. If its present value (after 2 years of depreciation) is ₹2,04,800, find its original value.", ["₹3,00,000", "₹3,10,000", "₹3,20,000", "₹3,30,000"], 2, "Original = 2,04,800 ÷ (0.80)² = 2,04,800 ÷ 0.64 = ₹3,20,000.", "MEDIUM"),
        ("The expenditure of a family is ₹36,000 per month. If it increases by 12%, what is the new expenditure?", ["₹39,920", "₹40,120", "₹40,320", "₹40,520"], 2, "New Exp = 36,000 × 1.12 = ₹40,320.", "EASY"),
        ("The population of a village increased by 5% in the first year and then decreased by 10% in the second year, resulting in a final population of 18,900. Find the original population.", ["19,500", "19,800", "20,000", "20,200"], 2, "Multiplier = 1.05 × 0.90 = 0.945. Original = 18,900 ÷ 0.945 = 20,000.", "MEDIUM"),
        ("A company increased the salary of its employees by 15%. If an employee's revised salary is ₹57,500, what was the original salary?", ["₹48,000", "₹49,000", "₹50,000", "₹52,000"], 2, "Original = 57,500 ÷ 1.15 = ₹50,000.", "EASY"),
        ("A's income is double B's income (100% more). By what percentage is B's income less than A's income?", ["25%", "33.33%", "50%", "66.67%"], 2, "Let B = 100 → A = 200. B is less by 100. % = (100 / 200) × 100 = 50%.", "EASY"),
        ("A shopkeeper offers two successive discounts of 25% and 10% on an article marked at ₹3,000. Find the final selling price.", ["₹1,975", "₹2,000", "₹2,025", "₹2,050"], 2, "SP = 3,000 × 0.75 × 0.90 = ₹2,025.", "EASY"),
        ("A quantity is increased by 12%, then decreased by 12%, and then increased by 5%. Find the overall percentage change (to two decimal places).", ["2.49% decrease", "3.49% increase", "3.49% decrease", "2.49% increase"], 1, "Multiplier = 1.12 × 0.88 × 1.05 = 1.03488 → 3.49% increase.", "MEDIUM"),
        ("In an election, Candidate A secured 52% of the valid votes and won by 2,400 votes. Find the total number of valid votes polled.", ["40,000", "50,000", "60,000", "75,000"], 2, "Winning margin = 52% - 48% = 4%. 4% = 2,400 → Total = (2,400 × 100) / 4 = 60,000.", "MEDIUM"),
        ("A number is increased successively by 15% and then 10%, resulting in a final value of 2,530. Find the original number.", ["1,800", "1,900", "2,000", "2,100"], 2, "Multiplier = 1.15 × 1.10 = 1.265. Original = 2,530 ÷ 1.265 = 2,000.", "EASY"),
        ("A candidate secured 72% marks in an examination and scored 576 marks. What is the maximum mark?", ["760", "780", "800", "820"], 2, "Max Marks = (576 × 100) / 72 = 800.", "EASY"),
        ("A shopkeeper offers two successive discounts of 10% and 20% on an article marked at ₹5,000. Find the final selling price.", ["₹3,500", "₹3,600", "₹3,700", "₹3,800"], 1, "SP = 5,000 × 0.90 × 0.80 = ₹3,600.", "EASY"),
        ("In an election between two candidates, the winning candidate secured 56% of the valid votes and won by 3,600 votes. Find the total number of valid votes polled.", ["24,000", "27,000", "30,000", "33,000"], 2, "Margin = 56% - 44% = 12%. Total = (3,600 ÷ 12) × 100 = 30,000.", "MEDIUM"),
        ("The population of a city increased by 15% in the first year and then decreased by 20% in the second year, resulting in a final population of 23,000. Find the original population.", ["24,000", "24,500", "25,000", "25,500"], 2, "Multiplier = 1.15 × 0.80 = 0.92. Original = 23,000 ÷ 0.92 = 25,000.", "MEDIUM"),
        ("If 18% of a number is 72, the number is:", ["360", "380", "400", "420"], 2, "Number = (72 × 100) / 18 = 400.", "EASY"),
        ("The value of a machine depreciates by 15% every year. If its present value is ₹2,89,000, what was its value one year ago?", ["₹3,20,000", "₹3,30,000", "₹3,40,000", "₹3,50,000"], 2, "Original = 2,89,000 ÷ 0.85 = ₹3,40,000.", "EASY"),
        ("The population of a city increases by 8% every year. If the present population is 1,25,000, what will be the population after one year?", ["1,33,000", "1,34,000", "1,35,000", "1,36,000"], 2, "Population = 1,25,000 × 1.08 = 1,35,000.", "EASY"),
        ("In an examination, Candidate A secures 42% marks and fails by 18 marks. Candidate B secures 54% marks and gets 42 marks more than passing mark. Find maximum marks.", ["450", "480", "500", "520"], 2, "0.54M - 0.42M = 18 + 42 → 0.12M = 60 → M = 500.", "MEDIUM"),
        ("A student obtained 468 marks out of 600 in an examination. What percentage of marks did the student score?", ["72%", "75%", "78%", "80%"], 2, "Percentage = (468 / 600) × 100 = 78%.", "EASY"),
        ("30 litres of a solution with 20% concentration is mixed with 10 litres of a solution with 50% concentration. Find concentration of resulting mixture.", ["25.5%", "26.5%", "27.5%", "28.5%"], 2, "Active = 6 + 5 = 11 L. Total = 40 L. % = (11 / 40) × 100 = 27.5%.", "MEDIUM"),
        ("The price of an article is increased by 10%, 20%, and 15% successively. What is the overall percentage increase?", ["48.8%", "50%", "51.8%", "52%"], 2, "100 × 1.10 × 1.20 × 1.15 = 151.8 → 51.8% increase.", "MEDIUM"),
        ("In an election between two candidates, winning candidate secured 58% valid votes and won by 6,400 votes. Find total valid votes polled.", ["36,000", "38,000", "40,000", "42,000"], 2, "Margin = 58% - 42% = 16%. Total = (6,400 ÷ 16) × 100 = 40,000.", "MEDIUM"),
        ("In an examination, Candidate A secures 40% marks and fails by 20 marks. Candidate B secures 55% marks and gets 40 marks more than pass mark. Find maximum marks.", ["300", "350", "400", "450"], 2, "0.15M = 60 → M = 400.", "MEDIUM"),
        ("A number is increased successively by 20% and then 25%, resulting in a final value of 3,000. Find the original number.", ["1,800", "1,900", "2,000", "2,100"], 2, "Multiplier = 1.20 × 1.25 = 1.50. Original = 3,000 ÷ 1.50 = 2,000.", "EASY"),
        ("A's income is 150% more than B's income. By what percentage is B's income less than A's income?", ["40%", "50%", "60%", "70%"], 2, "B is less by 150 / 250 = 60%.", "MEDIUM"),
        ("In an examination, 40% failed in Math, 30% in English, 15% in both. What percentage passed in both?", ["40%", "45%", "50%", "55%"], 1, "Failed at least one = 55% → Passed both = 45%.", "MEDIUM"),
        ("A number is decreased by 15% and then increased by 25%. Find overall percentage change.", ["4.25% increase", "6.25% increase", "8.25% increase", "10.25% increase"], 1, "0.85 × 1.25 = 1.0625 → 6.25% increase.", "EASY"),
        ("A school has 1,500 students. 48% are girls. If boys increase by 20% while girls remain same, new % of girls?", ["42.3%", "43.5%", "44.6%", "45.8%"], 1, "Girls = 720, New Total = 1656 → (720 / 1656) × 100 ≈ 43.5%.", "MEDIUM"),
        ("A number is increased by 40% and then decreased by 25%. Final value is:", ["5% less than original", "Equal to original", "5% greater than original", "10% greater than original"], 2, "100 × 1.40 × 0.75 = 105 → 5% greater than original.", "EASY")
    ]

    # 30 Graded Assessment (English)
    graded_en = [
        ("A commodity is increased by 15%, 10%, and 20% successively. The overall percentage increase is:", ["45%", "48%", "51.8%", "54%"], 2, "100 × 1.15 × 1.10 × 1.20 = 151.8 → 51.8% increase.", "MEDIUM"),
        ("A school has 1,200 students. If 55% are girls, how many boys are there?", ["520", "540", "560", "580"], 1, "Boys % = 45%. Number = (45 × 1200)/100 = 540.", "EASY"),
        ("The population increases successively by 10% and 20%. The overall increase is:", ["28%", "30%", "32%", "34%"], 2, "1.10 × 1.20 = 1.32 → 32% increase.", "EASY"),
        ("What is 35% of 640?", ["214", "224", "234", "244"], 1, "(35 × 640)/100 = 224.", "EASY"),
        ("A trader marks an article at ₹2,400 and allows a 25% discount. Find the selling price.", ["₹1,700", "₹1,750", "₹1,800", "₹1,850"], 2, "SP = 2,400 × 0.75 = ₹1,800.", "EASY"),
        ("A student scored 72 marks out of 90. What is the percentage of marks obtained?", ["75%", "78%", "80%", "82%"], 2, "(72 / 90) × 100 = 80%.", "EASY"),
        ("A shopkeeper first increases marked price of an article by 25% and then offers 20% discount. Compared to original price, customer pays:", ["5% less", "Same price", "5% more", "10% more"], 1, "1.25 × 0.80 = 1.00 (Same price).", "EASY"),
        ("A commodity is marked 40% above cost price and sold after allowing 10% discount. Profit percentage is:", ["22%", "24%", "26%", "28%"], 2, "CP = 100, MP = 140, SP = 126 → Profit % = 26%.", "MEDIUM"),
        ("Expenditure on fuel increases by 25%. By what percentage should consumption be reduced so total expenditure remains unchanged?", ["18%", "20%", "22%", "25%"], 1, "Reduction = (25 / 125) × 100 = 20%.", "MEDIUM"),
        ("A number is increased by 30% and then decreased by 20%. Overall percentage change is:", ["2% increase", "4% increase", "5% increase", "No change"], 1, "1.30 × 0.80 = 1.04 → 4% increase.", "EASY"),
        ("A number is increased by 30% and then decreased by 15%. Find overall percentage change.", ["10.5% increase", "12% increase", "15% increase", "18% increase"], 0, "1.30 × 0.85 = 1.105 → 10.5% increase.", "MEDIUM"),
        ("The population of a village increases by 10% every year. If present population is 8,000, what will be population after 2 years?", ["9,520", "9,600", "9,680", "9,720"], 2, "8,000 × (1.10)² = 8,000 × 1.21 = 9,680.", "EASY"),
        ("The price of a commodity increases by 20% and later decreases by 15%. Compared to original price, final price is:", ["2% increase", "2% decrease", "3% increase", "No change"], 0, "1.20 × 0.85 = 1.02 → 2% increase.", "EASY"),
        ("A trader purchased an article for ₹2,400. He marked it 30% above cost price and allowed 10% discount. What is profit %?", ["15%", "17%", "18%", "20%"], 1, "MP = 3,120, SP = 2,808. Profit = 408 → (408 / 2400) × 100 = 17%.", "MEDIUM"),
        ("A commodity is increased by 25% and then decreased by 25%. Net result is:", ["No change", "6.25% decrease", "5% decrease", "6.25% increase"], 1, "1.25 × 0.75 = 0.9375 → 6.25% decrease.", "EASY"),
        ("The population of a town increased by 20% in first year and 10% in second year. Total percentage increase over two years?", ["30%", "31%", "32%", "33%"], 2, "1.20 × 1.10 = 1.32 → 32% increase.", "EASY"),
        ("A trader buys two articles of same cost price. Sells one at 20% profit, other at 20% loss. Overall % profit/loss?", ["No profit no loss", "2% loss", "4% loss", "5% loss"], 0, "SP = 1.20x + 0.80x = 2.00x = CP → No profit no loss.", "EASY"),
        ("Price of petrol increases by 25%. By what percentage should consumption be reduced so total expenditure is unchanged?", ["18%", "20%", "22%", "25%"], 1, "Reduction = (25 / 125) × 100 = 20%.", "MEDIUM"),
        ("Shopkeeper offers two successive discounts of 20% and 10% on article marked at ₹2,000. Find final selling price.", ["₹1,380", "₹1,420", "₹1,440", "₹1,460"], 2, "SP = 2,000 × 0.80 × 0.90 = ₹1,440.", "EASY"),
        ("In examination, 30% failed in Math, 20% in English, 10% in both. Percentage who passed in both?", ["50%", "55%", "60%", "65%"], 2, "Failed at least one = 40% → Passed both = 60%.", "MEDIUM"),
        ("A number is increased successively by 10% and then 20%, resulting in final value of 2,640. Find original number.", ["1,800", "1,900", "2,000", "2,100"], 2, "Original = 2,640 ÷ 1.32 = 2,000.", "EASY"),
        ("Price of electricity increases by 25%. To keep expenditure constant, consumption should decrease by:", ["18%", "20%", "22%", "25%"], 1, "Decrease = (25 / 125) × 100 = 20%.", "MEDIUM"),
        ("A trader purchases an article for ₹1,800 and sells it for ₹2,160. Find profit percentage.", ["15%", "18%", "20%", "25%"], 2, "Profit = 360 → (360 / 1800) × 100 = 20%.", "EASY"),
        ("A's income is 25% more than B's income. By what percentage is B's income less than A's income?", ["16.67%", "20%", "25%", "33.33%"], 1, "(25 / 125) × 100 = 20%.", "EASY"),
        ("Population of a city decreases by 10% in first year and increases by 20% in second year. Overall percentage change is:", ["6% increase", "8% increase", "10% increase", "No change"], 1, "0.90 × 1.20 = 1.08 → 8% increase.", "EASY"),
        ("Population of a city decreases by 5% in one year and increases by 10% in next year. Overall % change is:", ["4.5% increase", "5% increase", "5.5% increase", "No change"], 0, "0.95 × 1.10 = 1.045 → 4.5% increase.", "EASY"),
        ("Candidate A secures 35% marks and fails by 25 marks. Candidate B secures 50% and gets 50 more than pass. Find maximum marks.", ["450", "475", "500", "525"], 2, "0.15M = 75 → M = 500.", "MEDIUM"),
        ("Income increases by 25%, expenditure increases by 10%. Initially earned ₹40,000 and spent ₹30,000. New saving?", ["₹16,000", "₹16,500", "₹17,000", "₹17,500"], 2, "New Income = 50,000, New Exp = 33,000 → New Saving = ₹17,000.", "MEDIUM"),
        ("Out of 50,000 voter base, candidate vote share increased from 40% to 46%. % increase in actual votes received?", ["10%", "12.5%", "15%", "17.5%"], 2, "Votes: 20,000 to 23,000 → (3,000 / 20,000) × 100 = 15%.", "MEDIUM"),
        ("In a class, 45% of students are girls. If there are 198 girls, find total number of students.", ["420", "430", "440", "450"], 2, "Total = (198 × 100) / 45 = 440.", "EASY")
    ]

    # 30 Worked Examples (Tamil)
    worked_ta = [
        ("ஒரு முதலீட்டின் மதிப்பு ₹75,000-இலிருந்து ₹84,000-ஆக அதிகரிக்கிறது. சதவீத அதிகரிப்பைக் காண்க.", ["10%", "11%", "12%", "15%"], 2, "அதிகரிப்பு = 84000 − 75000 = 9000. சதவீத அதிகரிப்பு = (9000/75000) × 100 = 12%. முக்கியக் கற்றல் கருத்து: சதவீத அதிகரிப்பு = (மதிப்பில் அதிகரிப்பு ÷ மூல மதிப்பு) × 100.", "EASY"),
        ("ஒரு கல்லூரியில் 40% மாணவர்கள் மாணவிகள். மாணவிகளின் எண்ணிக்கை மாறாமல் இருக்க, மாணவர்களின் (ஆண்கள்) எண்ணிக்கை 25% அதிகரித்தால், தற்போது மொத்த மாணவர்களில் மாணவிகள் எத்தனை சதவீதம்?", ["32%", "34.8%", "36%", "38%"], 1, "மொத்த மாணவர்கள் = 100. மாணவிகள் = 40, மாணவர்கள் = 60. புதிய ஆண்கள் = 60 × 1.25 = 75. புதிய மொத்தம் = 115. மாணவிகள் சதவீதம் = (40/115) × 100 = 34.8%.", "MEDIUM"),
        ("20% அமிலச் செறிவுள்ள 30 லிட்டர் கரைசல், 40% அமிலச் செறிவுள்ள 20 லிட்டர் கரைசலுடன் கலக்கப்படுகிறது. விளையும் கலவையின் அமிலச் செறிவைக் காண்க.", ["24%", "26%", "28%", "30%"], 2, "மொத்த அமிலம் = 6 + 8 = 14 லிட்டர். மொத்தக் கலவை = 50 லிட்டர். செறிவு = (14/50) × 100 = 28%.", "MEDIUM"),
        ("ஒரு பொருளின் விலை முதலில் 20% குறைக்கப்பட்டுப் பின்னர் 25% அதிகரிக்கப்படுகிறது. மூல விலையுடன் ஒப்பிடும்போது, இறுதி விலை", ["2% அதிகரிப்பு", "4% அதிகரிப்பு", "மாற்றமில்லை", "5% குறைவு"], 2, "மூல விலை = 100. குறைப்புக்குப் பின் = 80. அதிகரிப்புக்குப் பின் = 80 × 1.25 = 100. ஒட்டுமொத்த மாற்றம் இல்லை.", "EASY"),
        ("ஒரு பொருளின் விலை 12% அதிகரிக்கிறது. செலவு மாறாமல் இருக்க நுகர்வை எத்தனை சதவீதம் குறைக்க வேண்டும்?", ["10%", "10.71%", "12%", "12.5%"], 1, "தேவையான குறைப்பு = (12/112) × 100 = 10.71%.", "MEDIUM"),
        ("ஒரு கிராமத்தின் மக்கள்தொகை 15,000. அது 12% அதிகரித்தால், புதிய மக்கள்தொகை என்ன?", ["16,500", "16,700", "16,800", "17,000"], 2, "புதிய மக்கள்தொகை = 15000 × 112/100 = 16,800.", "EASY"),
        ("ஒரு வியாபாரி ஒரே அடக்க விலையுள்ள இரண்டு பொருட்களை வாங்குகிறார். ஒன்றை 40% இலாபத்திற்கும் மற்றொன்றை 10% நட்டத்திற்கும் விற்கிறார். அவரது ஒட்டுமொத்த இலாப அல்லது நட்டச் சதவீதத்தைக் காண்க.", ["10% இலாபம்", "15% இலாபம்", "10% நட்டம்", "15% நட்டம்"], 1, "மொத்த அடக்க விலை = 2x. மொத்த விற்பனை = 1.40x + 0.90x = 2.30x. ஒட்டுமொத்த இலாபம் % = (0.30 / 2) × 100 = 15% இலாபம்.", "EASY"),
        ("ஒரு வியாபாரி ஒரே அடக்க விலையுள்ள இரண்டு பொருட்களை வாங்குகிறார். ஒன்றை 30% இலாபத்திற்கும் மற்றொன்றை 10% நட்டத்திற்கும் விற்கிறார். அவரது ஒட்டுமொத்த இலாப அல்லது நட்டச் சதவீதத்தைக் காண்க.", ["5% இலாபம்", "10% இலாபம்", "5% நட்டம்", "10% நட்டம்"], 1, "ஒட்டுமொத்த இலாபம் % = ((2.20x - 2x)/2x) × 100 = 10% இலாபம்.", "EASY"),
        ("ஒரு வியாபாரி ஒரே அடக்க விலையுள்ள இரண்டு பொருட்களை வாங்குகிறார். ஒன்றை 25% இலாபத்திற்கும் மற்றொன்றை 15% நட்டத்திற்கும் விற்கிறார். அவரது ஒட்டுமொத்த இலாப அல்லது நட்டச் சதவீதத்தைக் காண்க.", ["5% இலாபம்", "5% நட்டம்", "10% இலாபம்", "10% நட்டம்"], 0, "ஒட்டுமொத்த இலாபம் % = ((2.10x - 2x)/2x) × 100 = 5% இலாபம்.", "EASY"),
        ("ஒரு பொருளின் விலை 25% அதிகரிக்கப்பட்டுப் பின்னர் 20% குறைக்கப்படுகிறது. மூல விலையுடன் ஒப்பிடும்போது, இறுதி விலை", ["5% அதிகரிப்பு", "5% குறைவு", "மாற்றமில்லை", "4% குறைவு"], 2, "மூல விலை = 100. 100 × 1.25 × 0.80 = 100. ஒட்டுமொத்த மாற்றம் இல்லை.", "EASY"),
        ("ஒரு குடும்பத்தின் செலவு 20% அதிகரிக்கிறது; அதன் வருமானம் 10% அதிகரிக்கிறது. முன்பு ₹30,000 வருமானத்தில் அக்குடும்பம் ₹6,000 சேமித்து வந்தால், புதிய சேமிப்பு என்ன?", ["₹3,600", "₹4,200", "₹4,800", "₹5,400"], 1, "மூலச் செலவு = ₹24,000. புதிய வருமானம் = ₹33,000. புதிய செலவு = ₹28,800. புதிய சேமிப்பு = ₹4,200.", "MEDIUM"),
        ("நிலையான 60,000 வாக்காளர்களைக் கொண்ட தொகுதியில், இரண்டு தேர்தல்களுக்கு இடையே ஒரு வேட்பாளரின் வாக்குப் பங்கு 25%-இலிருந்து 31%-ஆக அதிகரித்தது. அவர் பெற்ற உண்மையான வாக்குகளின் எண்ணிக்கையில் ஏற்பட்ட சதவீத அதிகரிப்பைக் காண்க.", ["20%", "22%", "24%", "26%"], 2, "முந்தைய வாக்குகள் = 15,000. தற்போதைய வாக்குகள் = 18,600. அதிகரிப்பு = 3,600. சதவீத அதிகரிப்பு = (3,600/15,000) × 100 = 24%.", "MEDIUM"),
        ("ஒரு தேர்வர் 480 மதிப்பெண்கள் பெற்று, மொத்த மதிப்பெண்ணின் 8% வித்தியாசத்தில் தோல்வியடைந்தார். தேர்ச்சி மதிப்பெண் 68% எனில், மொத்த மதிப்பெண் என்ன?", ["720", "750", "800", "840"], 2, "பெற்ற மதிப்பெண் = 68% - 8% = 60%. 60% = 480. மொத்த மதிப்பெண்கள் = (480 × 100) ÷ 60 = 800.", "MEDIUM"),
        ("சர்க்கரையின் விலை 25% குறைக்கப்படுகிறது. செலவு மாறாமல் இருக்க நுகர்வை எத்தனை சதவீதம் அதிகரிக்க வேண்டும்?", ["20%", "25%", "30%", "33⅓%"], 3, "தேவையான அதிகரிப்பு = (25/75) × 100 = 33⅓%.", "MEDIUM"),
        ("ஒரு நகரத்தின் மக்கள்தொகை முதல் ஆண்டில் 10%, இரண்டாம் ஆண்டில் 20% அதிகரித்து, மூன்றாம் ஆண்டில் 10% குறைகிறது. ஒட்டுமொத்தச் சதவீத மாற்றம் என்ன?", ["18.8% அதிகரிப்பு", "20% அதிகரிப்பு", "21% அதிகரிப்பு", "22% அதிகரிப்பு"], 0, "100 × 1.10 × 1.20 × 0.90 = 118.8 → 18.8% அதிகரிப்பு.", "MEDIUM"),
        ("ஓர் இயந்திரத்தின் மதிப்பு ஒவ்வோர் ஆண்டும் 10% தேய்மானம் அடைகிறது. அதன் தற்போதைய மதிப்பு ₹72,900 எனில், ஓர் ஆண்டுக்கு முன் அதன் மதிப்பு என்ன?", ["₹79,000", "₹80,000", "₹81,000", "₹82,000"], 2, "மூல மதிப்பு = 72,900 ÷ 0.90 = ₹81,000.", "EASY"),
        ("ஓர் இயந்திரத்தின் மதிப்பு 20% தேய்மானம் அடைகிறது. அதன் தற்போதைய மதிப்பு ₹48,000 எனில், தேய்மானத்திற்கு முன் அதன் மதிப்பைக் காண்க.", ["₹58,000", "₹60,000", "₹62,000", "₹64,000"], 1, "மூல மதிப்பு = 48,000 ÷ 0.80 = ₹60,000.", "EASY"),
        ("ஓர் இயந்திரத்தின் மதிப்பு ஒவ்வோர் ஆண்டும் 10% தேய்மானம் அடைகிறது. அதன் தற்போதைய மதிப்பு (3 ஆண்டுத் தேய்மானத்திற்குப் பின்) ₹2,50,047 எனில், அதன் மூல மதிப்பைக் காண்க.", ["₹3,23,000", "₹3,33,000", "₹3,43,000", "₹3,53,000"], 2, "மூல மதிப்பு = 2,50,047 ÷ 0.729 = ₹3,43,000.", "HARD"),
        ("ஓர் இயந்திரத்தின் மதிப்பு ஒவ்வோர் ஆண்டும் 10% தேய்மானம் அடைகிறது. அதன் தற்போதைய மதிப்பு (2 ஆண்டுத் தேய்மானத்திற்குப் பின்) ₹1,94,481 எனில், அதன் மூல மதிப்பைக் காண்க.", ["₹2,20,100", "₹2,30,100", "₹2,40,100", "₹2,50,100"], 2, "மூல மதிப்பு = 1,94,481 ÷ 0.81 = ₹2,40,100.", "HARD"),
        ("ஒருவரின் வருமானம் 20% அதிகரிக்கிறது; அவரது செலவு 15% அதிகரிக்கிறது. தொடக்கத்தில் அவர் தம் வருமானத்தில் 20% சேமித்தார். அவரது சேமிப்பு எத்தனை சதவீதம் அதிகரிக்கிறது?", ["20%", "30%", "40%", "50%"], 2, "வருமானம் = 100, சேமிப்பு = 20, செலவு = 80. புதிய வருமானம் = 120, புதிய செலவு = 92, புதிய சேமிப்பு = 28. சேமிப்பில் அதிகரிப்பு = ((28 - 20)/20) × 100 = 40%.", "MEDIUM"),
        ("ஒரு தேர்வில் 84% தேர்வர்கள் தேர்ச்சி பெற்றனர். 1,260 தேர்வர்கள் தேர்ச்சி பெற்றிருந்தால், தேர்வு எழுதியவர்கள் எத்தனை பேர்?", ["1,400", "1,450", "1,500", "1,550"], 2, "மொத்தத் தேர்வர்கள் = (1260 × 100) / 84 = 1,500.", "EASY"),
        ("15% உப்புச் செறிவுள்ள 40 லிட்டர் கரைசல், 35% உப்புச் செறிவுள்ள 10 லிட்டர் கரைசலுடன் கலக்கப்படுகிறது. விளையும் கலவையின் உப்புச் செறிவைக் காண்க.", ["17%", "19%", "21%", "23%"], 1, "மொத்த உப்பு = 6 + 3.5 = 9.5 லிட்டர். மொத்தக் கலவை = 50 லிட்டர். செறிவு = (9.5/50) × 100 = 19%.", "MEDIUM"),
        ("நிலையான 80,000 வாக்காளர்களைக் கொண்ட தொகுதியில், இரண்டு தேர்தல்களுக்கு இடையே ஒரு வேட்பாளரின் வாக்குப் பங்கு 35%-இலிருந்து 42%-ஆக அதிகரித்தது. அவர் பெற்ற உண்மையான வாக்குகளின் எண்ணிக்கையில் ஏற்பட்ட சதவீத அதிகரிப்பைக் காண்க.", ["15%", "18%", "20%", "22%"], 2, "முந்தைய வாக்குகள் = 28,000. தற்போதைய வாக்குகள் = 33,600. அதிகரிப்பு = 5,600. சதவீத அதிகரிப்பு = (5,600/28,000) × 100 = 20%.", "MEDIUM"),
        ("ஒரு தேர்வர் 45% மதிப்பெண்கள் பெற்று 30 மதிப்பெண்கள் வித்தியாசத்தில் தோல்வியடைகிறார். மற்றொரு தேர்வர் 60% மதிப்பெண்கள் பெற்றுத் தேர்ச்சி மதிப்பெண்ணைவிட 60 மதிப்பெண்கள் கூடுதலாகப் பெறுகிறார். மொத்த மதிப்பெண்கள்", ["500", "600", "700", "800"], 1, "சதவீத வேறுபாடு = 15%. மதிப்பெண் வேறுபாடு = 90. மொத்த மதிப்பெண்கள் = (90 × 100)/15 = 600.", "MEDIUM"),
        ("ஒரு போட்டித் தேர்வில் 35% தேர்வர்கள் கணிதத்திலும், 25% ஆங்கிலத்திலும், 15% இரண்டு பாடங்களிலும் தோல்வியடைந்தனர். 550 தேர்வர்கள் இரண்டு பாடங்களிலும் தேர்ச்சி பெற்றிருந்தால், மொத்தத் தேர்வர்களின் எண்ணிக்கையைக் காண்க.", ["900", "960", "1,000", "மேற்கண்ட எதுவுமில்லை"], 2, "குறைந்தது ஒன்றில் தோல்வி = 45%. இரண்டிலும் தேர்ச்சி = 55%. 55% = 550 → மொத்தம் = 1,000.", "HARD"),
        ("A-இன் வருமானம் B-இன் வருமானத்தைவிட 150% அதிகம். A-இன் வருமானத்தைவிட B-இன் வருமானம் எத்தனை சதவீதம் குறைவு?", ["40%", "50%", "60%", "70%"], 2, "B = 100 எனில் A = 250. B குறைவு = (150/250) × 100 = 60%.", "MEDIUM"),
        ("ஒரு தேர்வில், 40% தேர்வர்கள் கணிதத்திலும், 30% ஆங்கிலத்திலும், 15% இரண்டு பாடங்களிலும் தோல்வியடைந்தனர். இரண்டு பாடங்களிலும் தேர்ச்சி பெற்ற தேர்வர்கள் எத்தனை சதவீதம்?", ["40%", "45%", "50%", "55%"], 1, "குறைந்தது ஒன்றில் தோல்வி = 40 + 30 - 15 = 55%. இரண்டிலும் தேர்ச்சி = 100 - 55 = 45%.", "MEDIUM"),
        ("ஓர் எண் 15% குறைக்கப்பட்டுப் பின்னர் 25% அதிகரிக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத மாற்றத்தைக் காண்க.", ["4.25% அதிகரிப்பு", "6.25% அதிகரிப்பு", "8.25% அதிகரிப்பு", "10.25% அதிகரிப்பு"], 1, "ஒட்டுமொத்தப் பெருக்கக் காரணி = 0.85 × 1.25 = 1.0625 → 6.25% அதிகரிப்பு.", "EASY"),
        ("ஒரு பள்ளியில் 1,500 மாணவர்கள் உள்ளனர். அவர்களில் 48% மாணவிகள். மாணவிகளின் எண்ணிக்கை மாறாமல் இருக்க, மாணவர்களின் (ஆண்கள்) எண்ணிக்கை 20% அதிகரித்தால், மாணவிகளின் புதிய சதவீதம் என்ன?", ["42.3%", "43.5%", "44.6%", "45.8%"], 1, "மாணவிகள் = 720, புதிய மொத்தம் = 1656. மாணவிகளின் புதிய சதவீதம் = (720/1656) × 100 ≈ 43.5%.", "MEDIUM"),
        ("ஓர் எண் 40% அதிகரிக்கப்பட்டுப் பின்னர் 25% குறைக்கப்படுகிறது. இறுதி மதிப்பு", ["மூல மதிப்பைவிட 5% குறைவு", "மூல மதிப்புக்குச் சமம்", "மூல மதிப்பைவிட 5% அதிகம்", "மூல மதிப்பைவிட 10% அதிகம்"], 2, "100 × 1.40 × 0.75 = 105 → மூல மதிப்பைவிட 5% அதிகம்.", "EASY")
    ]

    # 30 Independent Practice (Tamil)
    indep_ta = [
        ("ஒரு நகரத்தின் மக்கள்தொகை முதல் ஆண்டில் 10% அதிகரித்து, பின்னர் இரண்டாம் ஆண்டில் 8% குறைந்து, இறுதி மக்கள்தொகை 20,240 ஆனது. மூல மக்கள்தொகையைக் காண்க.", ["19,500", "19,800", "20,000", "20,200"], 2, "ஒட்டுமொத்தப் பெருக்கக் காரணி = 1.10 × 0.92 = 1.012. மூல மக்கள்தொகை = 20,240 ÷ 1.012 = 20,000.", "MEDIUM"),
        ("ஒரு பொருளின் விலை 20% அதிகரிக்கப்பட்டுப் பின்னர் 10% குறைக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத மாற்றம்", ["8% அதிகரிப்பு", "10% அதிகரிப்பு", "12% அதிகரிப்பு", "2% அதிகரிப்பு"], 0, "100 × 1.20 × 0.90 = 108 → 8% அதிகரிப்பு.", "EASY"),
        ("ஓர் இயந்திரத்தின் மதிப்பு ஒவ்வோர் ஆண்டும் 20% தேய்மானம் அடைகிறது. அதன் தற்போதைய மதிப்பு (2 ஆண்டுத் தேய்மானத்திற்குப் பின்) ₹2,04,800 எனில், அதன் மூல மதிப்பைக் காண்க.", ["₹3,00,000", "₹3,10,000", "₹3,20,000", "₹3,30,000"], 2, "மூல மதிப்பு = 2,04,800 ÷ (0.80)² = 2,04,800 ÷ 0.64 = ₹3,20,000.", "MEDIUM"),
        ("ஒரு குடும்பத்தின் மாதச் செலவு ₹36,000. அது 12% அதிகரித்தால், புதிய செலவு என்ன?", ["₹39,920", "₹40,120", "₹40,320", "₹40,520"], 2, "புதிய செலவு = 36000 × 112/100 = ₹40,320.", "EASY"),
        ("ஒரு கிராமத்தின் மக்கள்தொகை முதல் ஆண்டில் 5% அதிகரித்து, பின்னர் இரண்டாம் ஆண்டில் 10% குறைந்து, இறுதி மக்கள்தொகை 18,900 ஆனது. மூல மக்கள்தொகையைக் காண்க.", ["19,500", "19,800", "20,000", "20,200"], 2, "ஒட்டுமொத்தப் பெருக்கக் காரணி = 1.05 × 0.90 = 0.945. மூல மக்கள்தொகை = 18,900 ÷ 0.945 = 20,000.", "MEDIUM"),
        ("ஒரு நிறுவனம் தன் ஊழியர்களின் சம்பளத்தை 15% உயர்த்தியது. ஓர் ஊழியரின் திருத்திய சம்பளம் ₹57,500 எனில், அவரது மூலச் சம்பளம் என்ன?", ["₹48,000", "₹49,000", "₹50,000", "₹52,000"], 2, "மூலச் சம்பளம் = 57,500 ÷ 1.15 = ₹50,000.", "EASY"),
        ("A-இன் வருமானம் B-இன் வருமானத்தைப்போல் இருமடங்கு (100% அதிகம்). A-இன் வருமானத்தைவிட B-இன் வருமானம் எத்தனை சதவீதம் குறைவு?", ["25%", "33.33%", "50%", "66.67%"], 2, "B = 100 எனில் A = 200. B குறைவு = (100/200) × 100 = 50%.", "EASY"),
        ("₹3,000 என விலை குறிக்கப்பட்ட ஒரு பொருளுக்கு, ஒரு கடைக்காரர் 25% மற்றும் 10% என இரண்டு தொடர்ச்சியான தள்ளுபடிகளை வழங்குகிறார். இறுதி விற்பனை விலையைக் காண்க.", ["₹1,975", "₹2,000", "₹2,025", "₹2,050"], 2, "இறுதி விற்பனை விலை = 3,000 × 0.75 × 0.90 = ₹2,025.", "EASY"),
        ("ஓர் அளவு 12% அதிகரிக்கப்பட்டு, பின்னர் 12% குறைக்கப்பட்டு, பின்னர் 5% அதிகரிக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத மாற்றத்தைக் காண்க.", ["2.49% குறைவு", "3.49% அதிகரிப்பு", "3.49% குறைவு", "2.49% அதிகரிப்பு"], 1, "ஒட்டுமொத்தப் பெருக்கக் காரணி = 1.12 × 0.88 × 1.05 = 1.03488 → 3.49% அதிகரிப்பு.", "MEDIUM"),
        ("ஒரு தேர்தலில் வேட்பாளர் A செல்லுபடியான வாக்குகளில் 52% பெற்று 2,400 வாக்குகள் வித்தியாசத்தில் வென்றார். பதிவான மொத்தச் செல்லுபடியான வாக்குகளின் எண்ணிக்கையைக் காண்க.", ["40,000", "50,000", "60,000", "75,000"], 2, "சதவீத வேறுபாடு = 52% - 48% = 4%. மொத்த வாக்குகள் = (2400 × 100)/4 = 60,000.", "MEDIUM"),
        ("ஓர் எண் தொடர்ச்சியாக 15% மற்றும் பின்னர் 10% அதிகரிக்கப்பட்டு, இறுதி மதிப்பு 2,530 ஆகிறது. மூல எண்ணைக் காண்க.", ["1,800", "1,900", "2,000", "2,100"], 2, "மூல எண் = 2,530 ÷ (1.15 × 1.10) = 2,530 ÷ 1.265 = 2,000.", "EASY"),
        ("ஒரு தேர்வர் ஒரு தேர்வில் 72% மதிப்பெண்களாக 576 மதிப்பெண்கள் பெற்றார். மொத்த மதிப்பெண் என்ன?", ["760", "780", "800", "820"], 2, "மொத்த மதிப்பெண்கள் = (576 × 100) / 72 = 800.", "EASY"),
        ("₹5,000 என விலை குறிக்கப்பட்ட ஒரு பொருளுக்கு, ஒரு கடைக்காரர் 10% மற்றும் 20% என இரண்டு தொடர்ச்சியான தள்ளுபடிகளை வழங்குகிறார். இறுதி விற்பனை விலையைக் காண்க.", ["₹3,500", "₹3,600", "₹3,700", "₹3,800"], 1, "இறுதி விற்பனை விலை = 5,000 × 0.90 × 0.80 = ₹3,600.", "EASY"),
        ("இரண்டு வேட்பாளர்களுக்கு இடையிலான ஒரு தேர்தலில், வெற்றி பெற்ற வேட்பாளர் செல்லுபடியான வாக்குகளில் 56% பெற்று 3,600 வாக்குகள் வித்தியாசத்தில் வென்றார். பதிவான மொத்தச் செல்லுபடியான வாக்குகளின் எண்ணிக்கையைக் காண்க.", ["24,000", "27,000", "30,000", "33,000"], 2, "வெற்றி வித்தியாசம் = 12%. மொத்த வாக்குகள் = (3,600 ÷ 12) × 100 = 30,000.", "MEDIUM"),
        ("ஒரு மாநகரத்தின் மக்கள்தொகை முதல் ஆண்டில் 15% அதிகரித்து, பின்னர் இரண்டாம் ஆண்டில் 20% குறைந்து, இறுதி மக்கள்தொகை 23,000 ஆனது. மூல மக்கள்தொகையைக் காண்க.", ["24,000", "24,500", "25,000", "25,500"], 2, "மூல மக்கள்தொகை = 23,000 ÷ (1.15 × 0.80) = 23,000 ÷ 0.92 = 25,000.", "MEDIUM"),
        ("ஓர் எண்ணின் 18% என்பது 72 எனில், அந்த எண்", ["360", "380", "400", "420"], 2, "எண் = (72 × 100) / 18 = 400.", "EASY"),
        ("ஓர் இயந்திரத்தின் மதிப்பு ஒவ்வோர் ஆண்டும் 15% தேய்மானம் அடைகிறது. அதன் தற்போதைய மதிப்பு ₹2,89,000 எனில், ஓர் ஆண்டுக்கு முன் அதன் மதிப்பு என்ன?", ["₹3,20,000", "₹3,30,000", "₹3,40,000", "₹3,50,000"], 2, "மூல மதிப்பு = 289000 ÷ 0.85 = ₹3,40,000.", "EASY"),
        ("ஒரு மாநகரத்தின் மக்கள்தொகை ஒவ்வோர் ஆண்டும் 8% அதிகரிக்கிறது. தற்போதைய மக்கள்தொகை 1,25,000 எனில், ஓர் ஆண்டுக்குப் பின் மக்கள்தொகை என்ன?", ["1,33,000", "1,34,000", "1,35,000", "1,36,000"], 2, "மக்கள்தொகை = 125000 × 108/100 = 1,35,000.", "EASY"),
        ("ஒரு தேர்வில், தேர்வர் A 42% மதிப்பெண்கள் பெற்று 18 மதிப்பெண்கள் வித்தியாசத்தில் தோல்வியடைகிறார். தேர்வர் B 54% மதிப்பெண்கள் பெற்றுத் தேர்ச்சி மதிப்பெண்ணைவிட 42 மதிப்பெண்கள் கூடுதலாகப் பெறுகிறார். மொத்த மதிப்பெண்களைக் காண்க.", ["450", "480", "500", "520"], 2, "0.54M - 0.42M = 18 + 42 → 0.12M = 60 → M = 500.", "MEDIUM"),
        ("ஒரு மாணவர் ஒரு தேர்வில் 600-க்கு 468 மதிப்பெண்கள் பெற்றார். அவர் பெற்ற மதிப்பெண் சதவீதம் என்ன?", ["72%", "75%", "78%", "80%"], 2, "சதவீதம் = (468/600) × 100 = 78%.", "EASY"),
        ("20% செறிவுள்ள 30 லிட்டர் கரைசல், 50% செறிவுள்ள 10 லிட்டர் கரைசலுடன் கலக்கப்படுகிறது. விளையும் கலவையின் செறிவைக் காண்க.", ["25.5%", "26.5%", "27.5%", "28.5%"], 2, "மொத்தச் செயல்படு கூறு = 6 + 5 = 11 லிட்டர். செறிவு = (11/40) × 100 = 27.5%.", "MEDIUM"),
        ("ஒரு பொருளின் விலை தொடர்ச்சியாக 10%, 20%, 15% அதிகரிக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத அதிகரிப்பு என்ன?", ["48.8%", "50%", "51.8%", "52%"], 2, "100 × 1.10 × 1.20 × 1.15 = 151.8 → 51.8% அதிகரிப்பு.", "MEDIUM"),
        ("இரண்டு வேட்பாளர்களுக்கு இடையிலான ஒரு தேர்தலில், வெற்றி பெற்ற வேட்பாளர் செல்லுபடியான வாக்குகளில் 58% பெற்று 6,400 வாக்குகள் வித்தியாசத்தில் வென்றார். பதிவான மொத்தச் செல்லுபடியான வாக்குகளின் எண்ணிக்கையைக் காண்க.", ["36,000", "38,000", "40,000", "42,000"], 2, "வெற்றி வித்தியாசம் = 16%. மொத்த வாக்குகள் = (6,400 ÷ 16) × 100 = 40,000.", "MEDIUM"),
        ("ஒரு தேர்வில், தேர்வர் A 40% மதிப்பெண்கள் பெற்று 20 மதிப்பெண்கள் வித்தியாசத்தில் தோல்வியடைகிறார். தேர்வர் B 55% மதிப்பெண்கள் பெற்றுத் தேர்ச்சி மதிப்பெண்ணைவிட 40 மதிப்பெண்கள் கூடுதலாகப் பெறுகிறார். மொத்த மதிப்பெண்களைக் காண்க.", ["300", "350", "400", "450"], 2, "0.15M = 60 → M = 400.", "MEDIUM"),
        ("ஓர் எண் தொடர்ச்சியாக 20% மற்றும் பின்னர் 25% அதிகரிக்கப்பட்டு, இறுதி மதிப்பு 3,000 ஆகிறது. மூல எண்ணைக் காண்க.", ["1,800", "1,900", "2,000", "2,100"], 2, "மூல எண் = 3,000 ÷ (1.20 × 1.25) = 3,000 ÷ 1.50 = 2,000.", "EASY"),
        ("A-இன் வருமானம் B-இன் வருமானத்தைவிட 150% அதிகம். A-இன் வருமானத்தைவிட B-இன் வருமானம் எத்தனை சதவீதம் குறைவு?", ["40%", "50%", "60%", "70%"], 2, "B குறைவு = (150/250) × 100 = 60%.", "MEDIUM"),
        ("ஒரு தேர்வில், 40% தேர்வர்கள் கணிதத்திலும், 30% ஆங்கிலத்திலும், 15% இரண்டு பாடங்களிலும் தோல்வியடைந்தனர். இரண்டு பாடங்களிலும் தேர்ச்சி பெற்ற தேர்வர்கள் எத்தனை சதவீதம்?", ["40%", "45%", "50%", "55%"], 1, "குறைந்தது ஒன்றில் தோல்வி = 55% → இரண்டிலும் தேர்ச்சி = 45%.", "MEDIUM"),
        ("ஓர் எண் 15% குறைக்கப்பட்டுப் பின்னர் 25% அதிகரிக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத மாற்றத்தைக் காண்க.", ["4.25% அதிகரிப்பு", "6.25% அதிகரிப்பு", "8.25% அதிகரிப்பு", "10.25% அதிகரிப்பு"], 1, "0.85 × 1.25 = 1.0625 → 6.25% அதிகரிப்பு.", "EASY"),
        ("ஒரு பள்ளியில் 1,500 மாணவர்கள் உள்ளனர். அவர்களில் 48% மாணவிகள். மாணவிகளின் எண்ணிக்கை மாறாமல் இருக்க, மாணவர்களின் (ஆண்கள்) எண்ணிக்கை 20% அதிகரித்தால், மாணவிகளின் புதிய சதவீதம் என்ன?", ["42.3%", "43.5%", "44.6%", "45.8%"], 1, "மாணவிகள் = 720, புதிய மொத்தம் = 1656. புதிய சதவீதம் = (720/1656) × 100 ≈ 43.5%.", "MEDIUM"),
        ("ஓர் எண் 40% அதிகரிக்கப்பட்டுப் பின்னர் 25% குறைக்கப்படுகிறது. இறுதி மதிப்பு", ["மூல மதிப்பைவிட 5% குறைவு", "மூல மதிப்புக்குச் சமம்", "மூல மதிப்பைவிட 5% அதிகம்", "மூல மதிப்பைவிட 10% அதிகம்"], 2, "100 × 1.40 × 0.75 = 105 → மூல மதிப்பைவிட 5% அதிகம்.", "EASY")
    ]

    # 30 Graded Assessment (Tamil)
    graded_ta = [
        ("ஒரு பொருளின் மதிப்பு தொடர்ச்சியாக 15%, 10%, 20% அதிகரிக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத அதிகரிப்பு", ["45%", "48%", "51.8%", "54%"], 2, "100 × 1.15 × 1.10 × 1.20 = 151.8 → 51.8% அதிகரிப்பு.", "MEDIUM"),
        ("ஒரு பள்ளியில் 1,200 மாணவர்கள் உள்ளனர். அவர்களில் 55% மாணவிகள் எனில், மாணவர்கள் (ஆண்கள்) எத்தனை பேர்?", ["520", "540", "560", "580"], 1, "மாணவர்கள் (ஆண்கள்) சதவீதம் = 45%. எண்ணிக்கை = (45 × 1200)/100 = 540.", "EASY"),
        ("மக்கள்தொகை தொடர்ச்சியாக 10% மற்றும் 20% அதிகரிக்கிறது. ஒட்டுமொத்த அதிகரிப்பு", ["28%", "30%", "32%", "34%"], 2, "1.10 × 1.20 = 1.32 → 32% அதிகரிப்பு.", "EASY"),
        ("640-இன் 35% என்ன?", ["214", "224", "234", "244"], 1, "(35 × 640)/100 = 224.", "EASY"),
        ("ஒரு வியாபாரி ஒரு பொருளுக்கு ₹2,400 என விலை குறித்து 25% தள்ளுபடி வழங்குகிறார். விற்பனை விலையைக் காண்க.", ["₹1,700", "₹1,750", "₹1,800", "₹1,850"], 2, "விற்பனை விலை = 2,400 × 0.75 = ₹1,800.", "EASY"),
        ("ஒரு மாணவர் 90-க்கு 72 மதிப்பெண்கள் பெற்றார். அவர் பெற்ற மதிப்பெண் சதவீதம் என்ன?", ["75%", "78%", "80%", "82%"], 2, "சதவீதம் = (72/90) × 100 = 80%.", "EASY"),
        ("ஒரு கடைக்காரர் முதலில் ஒரு பொருளின் குறித்த விலையை 25% உயர்த்திப் பின்னர் 20% தள்ளுபடி வழங்குகிறார். மூல விலையுடன் ஒப்பிடும்போது, வாடிக்கையாளர் செலுத்துவது", ["5% குறைவு", "அதே விலை", "5% அதிகம்", "10% அதிகம்"], 1, "1.25 × 0.80 = 1.00 (அதே விலை).", "EASY"),
        ("ஒரு பொருளுக்கு அடக்க விலையைவிட 40% அதிகமாக விலை குறிக்கப்பட்டு, 10% தள்ளுபடியுடன் விற்கப்படுகிறது. இலாபச் சதவீதம்", ["22%", "24%", "26%", "28%"], 2, "அடக்க விலை = 100, குறித்த விலை = 140, விற்பனை = 126 → இலாபம் = 26%.", "MEDIUM"),
        ("எரிபொருளின் விலை 25% அதிகரிக்கிறது. மொத்தச் செலவு மாறாமல் இருக்க நுகர்வை எத்தனை சதவீதம் குறைக்க வேண்டும்?", ["18%", "20%", "22%", "25%"], 1, "தேவையான குறைப்பு = (25/125) × 100 = 20%.", "MEDIUM"),
        ("ஓர் எண் 30% அதிகரிக்கப்பட்டுப் பின்னர் 20% குறைக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத மாற்றம்", ["2% அதிகரிப்பு", "4% அதிகரிப்பு", "5% அதிகரிப்பு", "மாற்றமில்லை"], 1, "1.30 × 0.80 = 1.04 → 4% அதிகரிப்பு.", "EASY"),
        ("ஓர் எண் 30% அதிகரிக்கப்பட்டுப் பின்னர் 15% குறைக்கப்படுகிறது. ஒட்டுமொத்தச் சதவீத மாற்றத்தைக் காண்க.", ["10.5% அதிகரிப்பு", "12% அதிகரிப்பு", "15% அதிகரிப்பு", "18% அதிகரிப்பு"], 0, "1.30 × 0.85 = 1.105 → 10.5% அதிகரிப்பு.", "MEDIUM"),
        ("ஒரு கிராமத்தின் மக்கள்தொகை ஒவ்வோர் ஆண்டும் 10% அதிகரிக்கிறது. தற்போதைய மக்கள்தொகை 8,000 எனில், 2 ஆண்டுகளுக்குப் பின் மக்கள்தொகை என்ன?", ["9,520", "9,600", "9,680", "9,720"], 2, "8,000 × (1.10)² = 8,000 × 1.21 = 9,680.", "EASY"),
        ("ஒரு பொருளின் விலை 20% அதிகரித்துப் பின்னர் 15% குறைகிறது. மூல விலையுடன் ஒப்பிடும்போது, இறுதி விலை", ["2% அதிகரிப்பு", "2% குறைவு", "3% அதிகரிப்பு", "மாற்றமில்லை"], 0, "1.20 × 0.85 = 1.02 → 2% அதிகரிப்பு.", "EASY"),
        ("ஒரு வியாபாரி ஒரு பொருளை ₹2,400-க்கு வாங்கினார். அடக்க விலையைவிட 30% அதிகமாக விலை குறித்து 10% தள்ளுபடி வழங்கினார். இலாபச் சதவீதம் என்ன?", ["15%", "17%", "18%", "20%"], 1, "குறித்த விலை = 3,120, விற்பனை = 2,808. இலாபம் = 408 → (408/2400) × 100 = 17%.", "MEDIUM"),
        ("ஒரு பொருளின் மதிப்பு 25% அதிகரிக்கப்பட்டுப் பின்னர் 25% குறைக்கப்படுகிறது. நிகர விளைவு", ["மாற்றமில்லை", "6.25% குறைவு", "5% குறைவு", "6.25% அதிகரிப்பு"], 1, "1.25 × 0.75 = 0.9375 → 6.25% குறைவு.", "EASY"),
        ("ஒரு நகரத்தின் மக்கள்தொகை முதல் ஆண்டில் 20%, இரண்டாம் ஆண்டில் 10% அதிகரித்தது. இரண்டு ஆண்டுகளில் மொத்தச் சதவீத அதிகரிப்பு என்ன?", ["30%", "31%", "32%", "33%"], 2, "1.20 × 1.10 = 1.32 → 32% அதிகரிப்பு.", "EASY"),
        ("ஒரு வியாபாரி ஒரே அடக்க விலையுள்ள இரண்டு பொருட்களை வாங்குகிறார். ஒன்றை 20% இலாபத்திற்கும் மற்றொன்றை 20% நட்டத்திற்கும் விற்கிறார். அவரது ஒட்டுமொத்த இலாப அல்லது நட்டச் சதவீதத்தைக் காண்க.", ["இலாபமும் இல்லை, நட்டமும் இல்லை", "2% நட்டம்", "4% நட்டம்", "5% நட்டம்"], 0, "விற்பனை = 2.00x = அடக்க விலை → இலாபமும் இல்லை, நட்டமும் இல்லை.", "EASY"),
        ("பெட்ரோலின் விலை 25% அதிகரிக்கிறது. மொத்தச் செலவு மாறாமல் இருக்க நுகர்வை எத்தனை சதவீதம் குறைக்க வேண்டும்?", ["18%", "20%", "22%", "25%"], 1, "தேவையான குறைப்பு = (25/125) × 100 = 20%.", "MEDIUM"),
        ("₹2,000 என விலை குறிக்கப்பட்ட ஒரு பொருளுக்கு, ஒரு கடைக்காரர் 20% மற்றும் 10% என இரண்டு தொடர்ச்சியான தள்ளுபடிகளை வழங்குகிறார். இறுதி விற்பனை விலையைக் காண்க.", ["₹1,380", "₹1,420", "₹1,440", "₹1,460"], 2, "இறுதி விற்பனை = 2,000 × 0.80 × 0.90 = ₹1,440.", "EASY"),
        ("ஒரு தேர்வில், 30% தேர்வர்கள் கணிதத்திலும், 20% ஆங்கிலத்திலும், 10% இரண்டு பாடங்களிலும் தோல்வியடைந்தனர். இரண்டு பாடங்களிலும் தேர்ச்சி பெற்ற தேர்வர்களின் சதவீதம்", ["50%", "55%", "60%", "65%"], 2, "தோல்வி = 40% → தேர்ச்சி = 60%.", "MEDIUM"),
        ("ஓர் எண் தொடர்ச்சியாக 10% மற்றும் பின்னர் 20% அதிகரிக்கப்பட்டு, இறுதி மதிப்பு 2,640 ஆகிறது. மூல எண்ணைக் காண்க.", ["1,800", "1,900", "2,000", "2,100"], 2, "மூல எண் = 2,640 ÷ 1.32 = 2,000.", "EASY"),
        ("மின்சாரத்தின் விலை 25% அதிகரிக்கிறது. செலவு மாறாமல் இருக்க, நுகர்வு குறைய வேண்டிய அளவு", ["18%", "20%", "22%", "25%"], 1, "தேவையான குறைப்பு = (25/125) × 100 = 20%.", "MEDIUM"),
        ("ஒரு வியாபாரி ஒரு பொருளை ₹1,800-க்கு வாங்கி ₹2,160-க்கு விற்கிறார். இலாபச் சதவீதத்தைக் காண்க.", ["15%", "18%", "20%", "25%"], 2, "இலாபம் = 360 → (360/1800) × 100 = 20%.", "EASY"),
        ("A-இன் வருமானம் B-இன் வருமானத்தைவிட 25% அதிகம். A-இன் வருமானத்தைவிட B-இன் வருமானம் எத்தனை சதவீதம் குறைவு?", ["16.67%", "20%", "25%", "33.33%"], 1, "(25/125) × 100 = 20%.", "EASY"),
        ("ஒரு மாநகரத்தின் மக்கள்தொகை முதல் ஆண்டில் 10% குறைந்து, இரண்டாம் ஆண்டில் 20% அதிகரிக்கிறது. ஒட்டுமொத்தச் சதவீத மாற்றம்", ["6% அதிகரிப்பு", "8% அதிகரிப்பு", "10% அதிகரிப்பு", "மாற்றமில்லை"], 1, "0.90 × 1.20 = 1.08 → 8% அதிகரிப்பு.", "EASY"),
        ("ஒரு மாநகரத்தின் மக்கள்தொகை ஓர் ஆண்டில் 5% குறைந்து, அடுத்த ஆண்டில் 10% அதிகரிக்கிறது. ஒட்டுமொத்தச் சதவீத மாற்றம்", ["4.5% அதிகரிப்பு", "5% அதிகரிப்பு", "5.5% அதிகரிப்பு", "மாற்றமில்லை"], 0, "0.95 × 1.10 = 1.045 → 4.5% அதிகரிப்பு.", "EASY"),
        ("ஒரு தேர்வில், தேர்வர் A 35% மதிப்பெண்கள் பெற்று 25 மதிப்பெண்கள் வித்தியாசத்தில் தோல்வியடைகிறார். தேர்வர் B 50% மதிப்பெண்கள் பெற்றுத் தேர்ச்சி மதிப்பெண்ணைவிட 50 மதிப்பெண்கள் கூடுதலாகப் பெறுகிறார். மொத்த மதிப்பெண்களைக் காண்க.", ["450", "475", "500", "525"], 2, "0.15M = 75 → M = 500.", "MEDIUM"),
        ("ஒருவரின் வருமானம் 25% அதிகரிக்கிறது; செலவு 10% அதிகரிக்கிறது. தொடக்கத்தில் அவர் ₹40,000 சம்பாதித்து ₹30,000 செலவு செய்தார். புதிய சேமிப்பு என்ன?", ["₹16,000", "₹16,500", "₹17,000", "₹17,500"], 2, "புதிய வருமானம் = 50,000, புதிய செலவு = 33,000 → புதிய சேமிப்பு = ₹17,000.", "MEDIUM"),
        ("நிலையான 50,000 வாக்காளர்களைக் கொண்ட தொகுதியில், இரண்டு தேர்தல்களுக்கு இடையே ஒரு வேட்பாளரின் வாக்குப் பங்கு 40%-இலிருந்து 46%-ஆக அதிகரித்தது. அவர் பெற்ற உண்மையான வாக்குகளின் எண்ணிக்கையில் ஏற்பட்ட சதவீத அதிகரிப்பைக் காண்க.", ["10%", "12.5%", "15%", "17.5%"], 2, "வாக்குகள்: 20,000-லிருந்து 23,000 → (3,000/20,000) × 100 = 15%.", "MEDIUM"),
        ("ஒரு வகுப்பில் 45% மாணவர்கள் மாணவிகள். 198 மாணவிகள் இருந்தால், மொத்த மாணவர்களின் எண்ணிக்கையைக் காண்க.", ["420", "430", "440", "450"], 2, "மொத்த மாணவர்கள் = (198 × 100)/45 = 440.", "EASY")
    ]

    out_lines = []
    out_lines.append("/* ============================================================================")
    out_lines.append("   ExamPro LMS - Percentage Course Seed Script (Bilingual: English & Tamil)")
    out_lines.append("   - 1 Course: Percentage / சதவீதம்")
    out_lines.append("   - 4 Assessments:")
    out_lines.append("       1. Percentage - Practice Set (English)   [60 Questions: 30 Worked + 30 Independent]")
    out_lines.append("       2. Percentage - Graded Assessment (English) [30 Questions: Assessment Q1-30]")
    out_lines.append("       3. சதவீதம் - பயிற்சித் தொகுப்பு (Tamil)      [60 Questions: 30 Worked + 30 Independent]")
    out_lines.append("       4. சதவீதம் - மதிப்பீட்டுத் தேர்வு (Tamil)     [30 Questions: Assessment Q1-30]")
    out_lines.append("   ============================================================================ */")
    out_lines.append("USE ExamProLMS;")
    out_lines.append("GO")
    out_lines.append("SET QUOTED_IDENTIFIER ON;")
    out_lines.append("GO\n")
    out_lines.append("BEGIN TRANSACTION;\n")
    out_lines.append("-- Clean existing Percentage course if present")
    out_lines.append("DELETE FROM dbo.Courses WHERE Slug IN (N'percentage', N'quantitative-aptitude');\n")
    out_lines.append("INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)")
    out_lines.append("VALUES (")
    out_lines.append("    N'Percentage / சதவீதம்',")
    out_lines.append("    N'percentage',")
    out_lines.append("    N'Comprehensive arithmetic module on percentages for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',")
    out_lines.append("    1")
    out_lines.append(");\n")
    out_lines = [
        "/* ============================================================================",
        "   ExamPro LMS - Percentage Course Seed Script (Unified Bilingual Model)",
        "   - 1 Course: Percentage / சதவீதம்",
        "   - 2 Assessments (Single unified assessment for both English & Tamil):",
        "       1. Percentage - Practice Set (percentage-practice) [60 Questions]",
        "          (30 Worked Examples + 30 Independent Practice in both English & Tamil)",
        "       2. Percentage - Graded Assessment (percentage-graded) [30 Questions]",
        "          (Assessment Questions 1-30 in both English & Tamil)",
        "   ============================================================================ */",
        "USE ExamProLMS;",
        "GO",
        "SET QUOTED_IDENTIFIER ON;",
        "GO\n",
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
        "GO\n",
        "BEGIN TRANSACTION;\n",
        "-- Clean previous Percentage courses and assessments",
        "DELETE FROM dbo.Assessments WHERE Slug IN (",
        "    N'percentage-practice', N'percentage-graded',",
        "    N'percentage-practice-en', N'percentage-graded-en',",
        "    N'percentage-practice-ta', N'percentage-graded-ta'",
        ");",
        "DELETE FROM dbo.Courses WHERE Slug IN (N'percentage', N'quantitative-aptitude');\n",
        "INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)",
        "VALUES (",
        "    N'Percentage / சதவீதம்',",
        "    N'percentage',",
        "    N'Comprehensive arithmetic module on percentages for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',",
        "    1",
        ");\n",
        "DECLARE @CourseId INT = SCOPE_IDENTITY();\n",
        "-- Insert ONLY 2 Assessments: 1 Practice and 1 Graded",
        "INSERT INTO dbo.Assessments (",
        "    CourseId, Title, TitleTa, Slug, Description, DescriptionTa, Topic, Difficulty,",
        "    DefaultDurationMinutes, MinDurationMinutes, TotalQuestions, PassPercentage,",
        "    AttemptType, SequentialUnlock, LockdownEnabled, ProctoringEnabled, OrderIndex",
        ")",
        "VALUES",
        "    (@CourseId, N'Percentage - Practice Set', N'சதவீதம் - பயிற்சித் தொகுப்பு', N'percentage-practice',",
        "     N'60 practice questions (Worked Examples + Independent Practice) with instant feedback & step-by-step solutions.',",
        "     N'60 பயிற்சிக் கணக்குகள் (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனடித் தீர்வுகளுடன்.',",
        "     N'Percentage', N'EASY', 60, 10, 60, 0, N'PRACTICE', 0, 0, 0, 1),",
        "    (@CourseId, N'Percentage - Graded Assessment', N'சதவீதம் - மதிப்பீட்டுத் தேர்வு', N'percentage-graded',",
        "     N'Official proctored & timed assessment on Percentage (30 Questions). Pass with 60% to master this topic.',",
        "     N'சதவீதத்திற்கான அதிகாரப்பூர்வக் கண்காணிப்புடன் கூடிய தேர்வு (30 வினாக்கள்). தேர்ச்சி 60%.',",
        "     N'Percentage', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 2);\n",
        "DECLARE @pracId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage-practice');",
        "DECLARE @gradId INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage-graded');\n"
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
                f"N'Percentage', {escape_sql(diff)}, {idx + 1})"
            )
            val_rows.append(row)
        out_lines.append(",\n".join(val_rows) + ";\n")

    # 1. Practice Set (60 Questions: 30 worked + 30 indep)
    insert_bilingual_questions("@pracId", worked_en + indep_en, worked_ta + indep_ta)

    # 2. Graded Assessment (30 Questions)
    insert_bilingual_questions("@gradId", graded_en, graded_ta)

    out_lines.append("COMMIT;")
    out_lines.append("PRINT 'Percentage Course seeded successfully: 1 Practice Assessment (60 Qs) and 1 Graded Assessment (30 Qs), fully bilingual (English & Tamil).';")
    out_lines.append("GO\n")

    output_path = r"c:\Users\Lenovo\Downloads\LMS\exampro-lms\database\04_percentage_bilingual_seed.sql"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Successfully wrote {output_path}")

if __name__ == "__main__":
    main()
