from datetime import datetime
import random
from user.models import User
from forum.models import Question, Tag, Content


TEXT = """用爱心来做事，用感恩的心做人。
人永远在追求快乐，永远在逃避痛苦。
有多大的思想，才有多大的能量。
人的能量=思想+行动速度的平方。
励志是给人快乐，激励是给人痛苦。
成功者绝不给自己软弱的借口。
你只有一定要，才一定会得到。
决心是成功的开始。
当你没有借口的那一刻，就是你成功的开始。
命运是可以改变的。
成功者绝不放弃。
成功永远属于马上行动的人。
下定决心一定要，才是成功的关键。
成功等于目标，其他都是这句话的注解。
成功是一个过程，并不是一个结果。
成功者学习别人的经验，一般人学习自己的经验。
只有第一名可以教你如何成为第一名。
学习需要有计划。
完全照成功者的方法来执行。
九十九次的理论不如一次的行动来得实际。
一个胜利者不会放弃，而一个放弃者永远不会胜利。
信心、毅力、勇气三者具备，则天下没有做不成的事。
如果你想得到，你就会得到，你所需要付出的只是行动。
一个缺口的杯子，如果换一个角度看它，它仍然是圆的。
对于每一个不利条件，都会存在与之相对应的有利条件。
一个人的快乐，不是因为他拥有的多，而是他计较的少。
世间成事，不求其绝对圆满，留一份不足，可得无限美好。
记住：你是你生命的船长；走自己的路，何必在乎其它。
你要做多大的事情，就该承受多大的压力。
如果你相信自己，你可以做任何事。
天空黑暗到一定程度，星辰就会熠熠生辉。
时间顺流而下，生活逆水行舟。
生活充满了选择，而生活的态度就是一切。
人各有志，自己的路自己走。
别人的话只能作为一种参考，是不能左右自己的。
成功来自使我们成功的信念。
相互了解是朋友，相互理解是知己。
没有所谓失败，除非你不再尝试。
有时可能别人不在乎你，但你不能不在乎自己。
你必须成功，因为你不能失败。
羡慕别人得到的，不如珍惜自己拥有的。
喜欢一个人，就该让他（她）快乐。
别把生活当作游戏，谁游戏人生，生活就惩罚谁，这不是劝诫，而是--规则！
你要求的次数愈多，你就越容易得到你要的东西，而且连带地也会得到更多乐趣。
把气愤的心境转化为柔和，把柔和的心境转化为爱，如此，这个世间将更加完美。
一份耕耘，一份收获，付出就有回报永不遭遇过失败，因我所碰到的都是暂时的挫折。
心如镜，虽外景不断变化，镜面却不会转动，这就是一颗平常心，能够景转而心不转。
每件事情都必须有一个期限，否则，大多数人都会有多少时间就花掉多少时间。
人，其实不需要太多的东西，只要健康地活着，真诚地爱着，也不失为一种富有。
生命之长短殊不重要，只要你活得快乐，在有生之年做些有意义的事，便已足够。
活在忙与闲的两种境界里，才能俯仰自得，享受生活的乐趣，成就人生的意义。
一个从来没有失败过的人，必然是一个从未尝试过什么的人。
待人退一步，爱人宽一寸，人生自然活得很快乐。
经验不是发生在一个人身上的事件，而是一个人如何看待发生在他身上的事。
加倍努力，证明你想要的不是空中楼阁。胜利是在多次失败之后才姗姗而来。
只要能执着远大的理想，且有不达目的绝不终止的意愿，便能产生惊人的力量。
一个人，只要知道付出爱与关心，她内心自然会被爱与关心充满。
如果我们可以改变情绪，我们就可以改变未来。
明白事理的人使自己适应世界，不明事理的人硬想使世界适应自己。
当困苦姗姗而来之时，超越它们会更有余味。
"""


def rand_content() -> str:
    return random.choice(TEXT.splitlines())


def test_data_import():
    # User.objects.all().delete()
    # Question.objects.all().delete()
    # Tag.objects.all().delete()
    # Content.objects.all().delete()
    users = []
    user_num = User.objects.all().count()
    for i in range(1+user_num, 19+user_num):
        u = User.objects.create(name=f'test{i}', account=f'account{i}', pwd=f'password{i}', identity=1, login_date='')
        users.append(u)
    for i in range(19+user_num, 21+user_num):
        u = User.objects.create(name=f'test{i}', account=f'account{i}', pwd=f'password{i}', identity=2, login_date='')
        users.append(u)
    questions = []
    question_num = Question.objects.all().count()
    for i in range(1+question_num, 11+question_num):
        q = Question.objects.create(title=f'question{i}', user=users[random.randint(0, 19)], published_time=datetime.now(), solved=random.randint(1, 10) > 8)
        Content.objects.create(user=q.user, published_time=datetime.now(), content=rand_content(), floor=1, questions=q, is_top=random.randint(1, 100) > 90)
        questions.append(q)
        if random.randint(0, 1) == 1:
            Tag.objects.create(question=q, name='tips')
        if random.randint(0, 1) == 1:
            Tag.objects.create(question=q, name='fake')
    for i in range(1, 100):
        c = Content.objects.create(user=users[random.randint(0, 19)], content=rand_content(), floor=0, published_time=datetime.now(), question=questions[random.randint(0, 9)], is_top=random.randint(1, 100) > 90)
        c.question.replied_time = datetime.now()
        if c.user.identity == 2:
            c.question.expert_reply = True
        c.question.save()
        all_contents = c.question.question_all_content.all()
        c.floor = all_contents.count()
        if random.randint(0, 1):
            c.replied_content_id = all_contents[random.randint(0, all_contents.count()-2)]
        c.save()
