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
    plt.savefig('Website/static/poll_results.png')
    plt.close('all')
    # plt.show()

# def graph(choices,responses):
#     thread.start_new_thread(graph_values(choices,responses),(choices,responses))

# a=['a','b']
# b=[69,6]
# graph(a,b)
