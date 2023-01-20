# KAU-AI
## 2022-1학기 AI입문 수업

## 유전 알고리즘(Genetic Algorithm)을 이용한 비밀번호 찾기

## 유전 알고리즘
- 유전 알고리즘은 자연세계의 진화과정을에 기초한 계산 모델로 최적화 문제를 해결하는 기법 중 하나이다. <sup>[[1]](#footnote_1)</sup>
- 적합도 평가, 돌연변이, 교배 연산 등으로 문제를 해결한다. 


### 1. Population(Chromosome) 만들기

- 진화 과정에서 환경에 적합한 종이 생존하기 때문에 여러 염색체를 생성해야 한다.

'''

    def word_generator(length):
        x = ''.join(random.sample(string.ascii_letters+string.digits,k=length))
        return x

    def population_generator(size, min_l, max_l):
        population = []
        for i in range(size):
            length = i % (max_l - min_l + 1) + min_l
            population.append(word_generator(length))
        return population


- 비밀번호는 문자와 숫자로 구성되어 있다고 가정하고 문자와 숫자를 무작위로 선택하여 염색체를 생성하였다.
- 비밀번호의 길이는 알 수 없지만, 너무 긴 비밀번호는 상당한 계산이 발생할 수 있기 때문에 최소 길이와 최대 길이를 설정하였다.


### 2. 적합도 평가 및 Chromosome 골라내기
- 진화 과정에서 살아남을 가치가 있는 염색체를 남기는 과정이다.

'''

    def fitness(password, test_word):
        score = 0
        if len(password) != len(test_word):
            return score

        len_score = 0.5
        score += len_score

        for i in range(len(password)):
            if password[i] == test_word[i]:
                score += 1
        return score / (len(password) + len_score) * 100
        
1. 비밀번호와 Chromosome의 길이가 다르면, 비밀번호를 맞출 수 없기 때문에 적합도는 0점이며, 
길이는 필수조건이기 때문에 이에 대한 점수는 0.5로 설정하였다.
2. 비밀번호와 Chromosome끼리 값을 비교 후, 일치하는 힝목 당 1점을 부여한 후, 100점 만점으로 환산하여 반환하였다.


'''
        
    def compute_perform(population,password):
        perform_list = []
        for i in population:
            score = fitness(password, i)

            if score > 0:
                pred_len = len(i)

            perform_list.append([i,score])

        population_sorted = sorted(perform_list, key=lambda x:x[1],reverse=True)
        return population_sorted, pred_len
        
        
3. 위와 같은 작업을 모든 Chromosome에 적용 후 점수를 기준으로 내림차순으로 정렬하여 반환하였다.


'''     
        
    def select_survivors(population_sorted, best_sample, lucky_few, password_len):
        next_generation = []

        for i in range(best_sample):
            if population_sorted[i][1] > 0:
                next_generation.append(population_sorted[i][0])

        lucky_survivors = random.sample(population_sorted, k=lucky_few)
        for j in lucky_survivors:
            next_generation.append(j[0])

        while len(next_generation) < best_sample + lucky_few:
            next_generation.append(word_generator(length=password_len))

        random.shuffle(next_generation)
        return next_generation        


4. 내림차순으로 정렬된 Chromosome 중에서 best_sample 수만큼만 남겼다.
5. 진화 과정에서도 그러하듯 최적의 Chromosome이 아니더라도 살아남을 Chromosome을 k개 선택하였다.
6. 앞선 작업을 거친 후에도 초기에 설정한 개체수에 도달하지 못하면, 새로운 개체를 생성하였다.
        

### 3. 교배(Crossover)를 통한 자식 생성




    



 # Reference
<a name="footnote_1">[1]</a>  :  wikipedia
