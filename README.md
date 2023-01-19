# KAU-AI
## 2022-1학기 AI입문 수업

### 유전 알고리즘(Genetic Algorithm)을 이용한 비밀번호 찾기

### 유전 알고리즘
- 유전 알고리즘은 자연세계의 진화과정을에 기초한 계산 모델로 최적화 문제를 해결하는 기법 중 하나이다. <sup>[[1]](#footnote_1)</sup>
- 적합도 평가, 돌연변이, 교배 연산 등으로 문제를 해결한다. 

1. Population(Chromosome) 만들기
- 진화 과정에서 환경에 적합한 종이 생존하기 때문에 여러 염색체를 생성해야 한다.


''' python
    def word_generator(length):
        x = ''.join(random.sample(string.ascii_letters+string.digits,k=length))
        return x

    def population_generator(size, min_l, max_l):
        population = []
        for i in range(size):
            length = i % (max_l - min_l + 1) + min_l
            population.append(word_generator(length))
        return population
'''

- 비밀번호는 문자와 숫자로 구성되어 있다고 가정하고 문자와 숫자를 무작위로 선택하여 염색체를 생성하였다.
- 비밀번호의 길이는 알 수 없지만, 너무 긴 비밀번호는 상당한 계산이 발생할 수 있기 때문에 최소 길이와 최대 길이를 설정하였다.


2. 적합도 평가
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
'''




 # Reference
<a name="footnote_1">[1]</a>  :  wikipedia
