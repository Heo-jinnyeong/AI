import random
import string

"""

비밀번호 맞추기 with genetic algorithm
2018126132 허진녕

"""

# population (chromosome) 만들기

# password = 'moondol2'
# min_l = 8
# max_l = 12

def word_generator(length):
    x = ''.join(random.sample(string.ascii_letters+string.digits,k=length))
    return x

def population_generator(size, min_l, max_l):
    population = []
    for i in range(size):
        length = i % (max_l - min_l + 1) + min_l
        population.append(word_generator(length))
    return population

# pop = population_generator(size=100, min_l=min_l,max_l=max_l)


# 적합도 평가(fitness function) 함수 만들기

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


# 적합한 종자 골라내기

def compute_perform(population,password):
    perform_list = []
    for i in population:
        score = fitness(password, i)
        
        if score > 0:
            pred_len = len(i)

        perform_list.append([i,score])

    population_sorted = sorted(perform_list, key=lambda x:x[1],reverse=True)
    return population_sorted, pred_len

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

# pop_sorted, pred_len = compute_perform(pop,password)
# survivors = select_survivors(pop_sorted, best_sample=20, lucky_few=20,password_len=pred_len)


# 새로운 세대(자식) 만들기

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


# 돌연변이(mutation) 만들기

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


# PASSWORD 찾기

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