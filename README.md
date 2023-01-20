# KAU-AI
## 2022-1학기 AI입문 수업

## 유전 알고리즘(Genetic Algorithm)을 이용한 비밀번호 찾기

## 유전 알고리즘
- 유전 알고리즘은 자연세계의 진화과정을에 기초한 계산 모델로 최적화 문제를 해결하는 기법 중 하나이다. <sup>[[1]](#footnote_1)</sup>
- 적합도 평가, 돌연변이, 교배 연산 등으로 문제를 해결한다. 

&nbsp;

# 1. Population(Chromosome) 

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

&nbsp;

# 2. 적합도 평가 및 Chromosome 선택
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
        
&nbsp;

# 3. 교배(Crossover)를 통한 자식 생성

'''

    def create_child(parent1, parent2):
        child = ''
        min_len_parent = min(len(parent1),len(parent2))
        for i in range(min_len_parent):
            if (int(100*random.random()) < 50):
                child += parent1[i]
            else:
                child += parent2[i]
        return child

    def create_children(parents, n_child):
        next_population = []
        for i in range(int(len(parents)/2)):
            for j in range(n_child):
                next_population.append(create_child(parents[i],parents[len(parents)-1-i]))
        return next_population



1. 다음 세대로 넘어가기 위해서는 교배(Crossover)가 필요하며, 두 개의 Chromosome에서 무작위로 정보를 추출하여 자식 Chromosome을 만들었다.
2. 부모 Chromosome을 고를 때 중복되지 않도록 양끝에서 하나씩 순차적으로 선택하였다.

&nbsp;

# 4. 돌연변이(Mutatio) 

'''

    def mutate_word(word):
        idx = int(random.random()*len(word))
        if (idx==0):
            word = random.choice(string.ascii_letters+string.digits) + word[1:]
        else:
            word = word[:idx] + random.choice(string.ascii_letters+string.digits) + word[idx+1:]
        return word

    def mutate_population(population, chance_of_mutation):
        for i in range(len(population)):
            if random.random() * 100 < chance_of_mutation:
                population[i] = mutate_word(population[i])
        return population
    

1. 돌연변이를 생성할 때, 문자에서 임의로 하나를 선택하여 변경하였다.
2. 돌연변이 발생할 확률은 chance_of_mutation으로 정해주었다.

&nbsp;

# 5. 실행


'''

    password = 'moondol2'
    min_l = 8
    max_l = 12
    n_generation = 300
    population = 100
    best_sample = 20
    lucky_few = 20
    n_child = 5
    chance_of_mutation = 10

    pop = population_generator(size=population,min_l=min_l,max_l=max_l)

    for i in range(n_generation):

        pop_sorted, pred_len = compute_perform(population=pop,password=password)

        if int(pop_sorted[0][1]) == 100:
            print('success')
            print(pop_sorted[0][0])
            break

        survivors = select_survivors(population_sorted=pop_sorted,best_sample=best_sample,lucky_few=lucky_few,password_len=pred_len)

        children = create_children(parents=survivors,n_child=n_child)

        new_generation = mutate_population(population=children,chance_of_mutation=chance_of_mutation)

        pop = new_generation

        print(i)
        print(pop_sorted[0])

![그림1](https://user-images.githubusercontent.com/94584793/213619255-1082ac87-887b-4487-9e78-14c7914c4604.png)




위와 같이 변수를 설정한 후 프로그램을 실행시키면 유전 알고리즘을 이용한 비밀번호 탐색이 시직된다.
초기값에 따라 추론 시간이 달라진다는 단점이 있지만, 이러한 비정혁적 특징으로 수식으로 설명하기 어려운 문제를 해결할 수 있다는 장점이 있다.




 # Reference
<a name="footnote_1">[1]</a>  :  wikipedia
