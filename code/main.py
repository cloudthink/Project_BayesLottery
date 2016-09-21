__author__ = 'think'
# -*- coding: utf-8 -*-

# data

import csv

file_address = 'C:/Users/think/Desktop'
regular_season_results = csv.reader(open(file_address + '/project/regular_season_results.csv', 'r'))
seasons = csv.reader(open(file_address + '/project/seasons.csv', 'r'))
teams = csv.reader(open(file_address + '/project/teams.csv', 'r'))
tourney_results = csv.reader(open(file_address + '/project/tourney_results.csv', 'r'))
tourney_seeds = csv.reader(open(file_address + '/project/tourney_seeds.csv', 'r'))
tourney_slots = csv.reader(open(file_address + '/project/tourney_slots.csv', 'r'))

#赛季对应的年份数据
seasons_line=[]
years_line=[]
for line in seasons:
    if line[0] != 'season':  #去掉汉字
        seasons_line.append(line[0])
        years_line.append(line[1])
#常规赛数据
regular_results_line = []
for line in regular_season_results:
    if line[0] != 'season':  #去掉汉字
        regular_results_line.append((line[0], line[2], line[4]))
#淘汰赛数据
tourney_seeds_line = []
seeds_season = {}
seeds_season_two = {}
teams_seed = {}
seed_teams = {}
for line in tourney_seeds:
    if line[0] != 'season':  #去掉汉字
        teams_seed[line[2]] = line[1]
        seeds_season[line[0]] = teams_seed
        seed_teams[line[1]] = line[2]
        seeds_season_two[line[0]] = seed_teams
tourney_results_line = []
for line in tourney_results:
    if line[0] != 'season':  #去掉汉字
        tourney_results_line.append((line[0], line[1], line[2], line[4]))
#淘汰赛种子排名数据
tourney_slots_line = {}
slots_lines = []
slots_team = []
for line in tourney_slots:
    if line[0] != 'slot':  #去掉汉字
        slots_team = (line[1], line[2])
        tourney_slots_line[line[0]] = slots_team
        slots_lines.append(line[0])

#某队伍在当前season的胜率Pi计算
def p(season, team_id):                                 #传入入season，team_id，类型为字符串
    win_number = lose_number = 0
    p_i_win = 0.000
    for one in regular_results_line:
        if one[0] == season:
            if one[1] == team_id:
                win_number = win_number + 1
            if one[2] == team_id:
                lose_number = lose_number + 1
    p_i_win = win_number / (win_number + lose_number)
    return (p_i_win)

#A队与B队比赛，A队胜利的概率
def pab(season, team_a, team_b):
    pa = p(season, team_a)
    pb = p(season, team_b)
    #print('rrr',pa)
    pa = float(pa)
    pb = float(pb)
    pawinb = (pa * (1 - pb)) / (pa * (1 - pb) + (1 - pa) * pb)
    return pawinb


#构建淘汰赛竞赛图生成，可查看code_result.pdf文件
def tourney_tree(season):
    one_line = []
    two_line = []
    three_line = []
    four_line = []
    five_line = []
    six_line = []
    pre_maybe_true_num=0
    tourney_num=0
    for one in tourney_results_line:
        if one[0] == season:
            tourney_num=tourney_num+1
            if one[1] == ('136' or '137'):
                one_line.append((one[2], seeds_season[season][one[2]], one[3], seeds_season[season][one[3]],pab(season,one[2],one[3])))
                if(pab(season,one[2],one[3]))>0.5:
                    pre_maybe_true_num=pre_maybe_true_num+1
            if one[1] == ('138' or '139'):
                two_line.append((one[2], seeds_season[season][one[2]], one[3], seeds_season[season][one[3]],pab(season,one[2],one[3])))
                if(pab(season,one[2],one[3]))>0.5:
                    pre_maybe_true_num=pre_maybe_true_num+1
            if one[1] == ('143' or '144'):
                three_line.append((one[2], seeds_season[season][one[2]], one[3], seeds_season[season][one[3]],pab(season,one[2],one[3])))
                if(pab(season,one[2],one[3]))>0.5:
                    pre_maybe_true_num=pre_maybe_true_num+1
            if one[1] == ('145' or '146'):
                four_line.append((one[2], seeds_season[season][one[2]], one[3], seeds_season[season][one[3]],pab(season,one[2],one[3])))
                if(pab(season,one[2],one[3]))>0.5:
                    pre_maybe_true_num=pre_maybe_true_num+1
            if one[1] == '152':
                five_line.append((one[2], seeds_season[season][one[2]], one[3], seeds_season[season][one[3]],pab(season,one[2],one[3])))
                if(pab(season,one[2],one[3]))>0.5:
                    pre_maybe_true_num=pre_maybe_true_num+1
            if one[1] == '154':
                six_line.append((one[2], seeds_season[season][one[2]], one[3], seeds_season[season][one[3]],pab(season,one[2],one[3])))
                if(pab(season,one[2],one[3]))>0.5:
                    pre_maybe_true_num=pre_maybe_true_num+1
    print('Season:',season)
    print('Round 1:\n',one_line)
    print('Round 2:\n',two_line)
    print('Round 3:\n',three_line)
    print('Round 4:\n',four_line)
    print('Round 5:\n',five_line)
    print('Round 6:\n',six_line)
    score=pre_maybe_true_num/float(tourney_num)
    print('the true percentage of peoples predict:',score)
    return score

score_line=[]
for one_season in seasons_line:
    score=tourney_tree(one_season)
    score_line.append((one_season,score))
print('all season score:')
max_score=0
for one in score_line:
    print(one)
    if one[1]>max_score:
        max_score=one[1]
        max_season=one[0]
print('result:',max_season,years_line[seasons_line.index(max_season)],max_score)






#csvfile.close()
