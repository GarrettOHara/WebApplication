# @routes.route('results', methods=['GET', 'POST'])
# def results():
#     if request.method == 'GET':
#         question = session['qid']
#         sql = text(
#             """
#             SELECT q.text as Question, c.text AS Choice, COUNT(c.choice_id)-1 AS Responses
#             FROM question AS q, choice AS c, answer as a
#             WHERE a.question_id = q.question_id and a.choice_id = c.choice_id and q.question_id = {}
#             GROUP BY a.choice_id;
#             """.format(question)
#         )
#         result = db.engine.execute(sql)

#         responses = []
#         choices = []
#         question = ""
#         print("RESULTS:")
#         for r in result:
#             responses.append(r['Responses'])
#             choices.append(r['Choice'])

#         # ORIGINAL GRAPHING METHOD
#         th = thread.Thread(target=results_graph.graph_values,args=(choices,responses), daemon=True)
#         th.start()
#         time.sleep(1)


#         # ALTERNATIVE GRAPHING METHOD (NOT FINISHED, AT BOTTOM OF FILE)
#         # thread = Thread(target=plot_png)
#         # thread.start()
#         # thread.join()
#         # time.sleep(1)
#         # import base64
#         # data_uri = base64.b64encode(open('Website/static/poll_results.png', 'rb').read()).decode('utf-8')
#         # img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
#         # print(img_tag)
#         return render_template("results.html")#,file=img_tag)

# """
# The code below is a possibility of fixing the graph

# You can create matplot graphs like this instead of saving the image
# """
# # import io
# # import random
# # from flask import Response
# # from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# # from matplotlib.figure import Figure
# # import matplotlib
# # import matplotlib.pyplot as plt
# # matplotlib.use('Agg')

# # @routes.route('/plot.png')
# # def plot_png():
# #     question = session['qid']
# #     sql = text(
# #         """
# #         SELECT q.text as Question, c.text AS Choice, COUNT(c.choice_id)-1 AS Responses
# #         FROM question AS q, choice AS c, answer as a
# #         WHERE a.question_id = q.question_id and a.choice_id = c.choice_id and q.question_id = {}
# #         GROUP BY a.choice_id;
# #         """.format(question)
# #     )
# #     result = db.engine.execute(sql)

# #     responses = []
# #     choices = []
# #     question = ""
# #     print("RESULTS:")
# #     for r in result:
# #         responses.append(r['Responses'])
# #         choices.append(r['Choice'])

# #     # th = thread.Thread(target=results_graph.graph_values,args=(choices,responses), daemon=True)
# #     # th.start()
# #     # time.sleep(4)
# #     thread = Thread(target=plot_png)
# #     thread.start()
# #     thread.join()
# #     time.sleep(1)


# #     fig = create_figure(responses,choices)
# #     output = io.BytesIO()
# #     FigureCanvas(fig).print_png(output)
# #     return Response(output.getvalue(), mimetype='image/png')

# # """
# # We could have the graph created in here
# # This is a simple example
# # """
# # def create_figure(responses,choices):
# #     # print(len(responses))
# #     # fig = Figure()
# #     # axis = fig.add_subplot(1, 1, 1)
# #     # xs = range(100)
# #     # ys = [random.randint(1, 50) for x in xs]
# #     # axis.plot(xs, ys)
# #     # return fig

# #     fig = Figure()
# #     x_pos = [i for i, _ in enumerate(choices)]
# #     plt.xticks(x_pos, choices)
# #     plt.bar(x_pos,responses)
# #     # plt.title(question)
# #     plt.xlabel("Choices")
# #     plt.ylabel("Responses")
# #     # name = create_image_name()
# #     plt.savefig('Website/static/{}.png'.format("poll_results"))
# #     plt.close('all')
# #     return fig