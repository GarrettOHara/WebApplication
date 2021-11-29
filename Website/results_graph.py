import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
# import _threasd as thread


# PASS IN OPTIONS AND RESULTS AS LISTS WITH COORESPONDING INDICIES
def graph_values(choices, responses):
    print(choices)
    print(responses)
    plt.figure().clear()
    x_pos = [i for i, _ in enumerate(choices)]
    plt.xticks(x_pos, choices)
    plt.bar(x_pos,responses)
    # plt.title(question)
    plt.xlabel("Choices")
    plt.ylabel("Responses")
    # name = create_image_name()
    plt.savefig('Website/static/{}.png'.format("poll_results"))
    plt.close('all')
    # return name
    # plt.show()

def create_image_name():
    import datetime
    basename = "poll_results"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    return "_".join([basename, suffix])

# def graph(choices,responses):
#     thread.start_new_thread(graph_values(choices,responses),(choices,responses))

# a=['a','b']
# b=[69,6]
# graph(a,b)
