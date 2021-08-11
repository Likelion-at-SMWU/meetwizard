from django import shortcuts

#스케줄을 진한 빨강,옅은 빨강, 진한 녹색, 옅은 녹색으로 취합하는 함수
def scheduleDivideIntoFour(memberSchedules, userCnt: int):
    from meet.algorithm.main import MemberSchedule

    #day->time->user 기준으로 정렬
    sorted_data = sorted(memberSchedules, key=lambda memberSchedule: (memberSchedule.day, memberSchedule.time, memberSchedule.member))


    #변수 초기화
    result_list = []
    prev_day = sorted_data[0].day
    prev_time = sorted_data[0].time
    prev_member = sorted_data[0].member
    red_cnt = 0
    green_cnt = 0

    #스케줄 취합
    for schedule in sorted_data:
        if (prev_day != schedule.day or prev_time != schedule.time):    #day나 time이 달라지면 이전 값 저장하고 변수들 초기화
            #이전 값 저장
            v = 0   #초기값은 0
            if (red_cnt == userCnt): v = -1         #모두 red라면 진한 빨강
            elif (red_cnt > 0): v = -1 * (red_cnt / userCnt)  #red가 하나라도 있으면 옅은 빨강(개수에 비례함)
            elif (green_cnt == userCnt): v = 1      #모두 green이라면 진한 녹색
            elif (green_cnt > 0): v = green_cnt / userCnt #red는 없고 green만 일부 있으면 옅은 녹색(개수에 비례함)
            result_list.append(MemberSchedule(member=0, day=prev_day, time=prev_time, value=v)) #result_list에 추가

            #변수 초기화
            prev_day = schedule.day
            prev_time = schedule.time
            red_cnt = 0
            green_cnt = 0
            
        if (schedule.value == -1):  #red + 1
            red_cnt += 1
        elif (schedule.value == 1): #green + 1
            green_cnt += 1

    #for문 종료 후 마지막 값 저장
    if (red_cnt == userCnt): v = -1         #모두 red라면 진한 빨강
    elif (red_cnt > 0): v = -1 * (red_cnt / userCnt)  #red가 하나라도 있으면 옅은 빨강(개수에 비례함)
    elif (green_cnt == userCnt): v = 1      #모두 green이라면 진한 녹색
    elif (green_cnt > 0): v = green_cnt / userCnt #red는 없고 green만 일부 있으면 옅은 녹색(개수에 비례함)

    result_list.append(MemberSchedule(member=0, day=prev_day, time=prev_time, value=v))   #마지막 결과 result_list에 추가
    
    return result_list


