calibration_matrix = [[5588, 6668, 8592, 5205], [7299, 8443, 10338, 6877], [9019, 10230, 12095, 8560]]
calibration_matrix_adjusted = [[5588, 6668, 8592, 5205], [7299, 8443, 10338, 6877], [9019, 10230, 12095, 8560]]

TOP_RIGHT = 0
BOTTOM_RIGHT = 1
TOP_LEFT = 2
BOTTOM_LEFT = 3

#Raw_1 intervals
#               0           1.1         BLOCO           1           1               1               preto
intervals_1 = [[0, 321], [381, 1136], [1325, 1575], [1764, 2003], [2183, 2392], [2522, 8768], [8929, 9227],
               [9376, 9554], [9737, 9949], [10208, 10466], [10614, 10900], [11183, 11405], [11642, 16178]]
#               preto           preto           cinza         preto           preto           preto

    # Pesos

weights = [0, 1.1, 8.5, 1.0, 1.0, 1.0, 1.43, 1.43, 1.43, 2.2, 1.43, 1.43, 1.43]
cumu_weight = [0, 1.1, 9.6, 10.6, 11.6, 12.6, 14.03, 15.46, 16.89, 19.09, 20.52, 21.95, 23.38]

#Raw_2 intervals

intervals_2 = [[95, 951], [1071, 2225], [2775, 4254], [4620, 5456], [5690, 6553], [6931, 7738], [8561, 8917],
               [9154, 9952], [10387, 11054], [11821, 12571], [12787, 13199], [13427, 13728], [13965, 14179],
               [14316, 14517], [14655, 14852], [15007, 15248], [15338, 15593], [15758, 16358], [16481, 17339]]

weights_2 = [0, 1.1, 8.5, 1.43, 1.43, 1.43, 1.43, 1.43, 1.43, 2.2, -2.2, -1.43, -1.43, -1.43, -1.43, -1.43, -1.43, -8.5, -1.1, 0]
cumu_weight_2 = [0, 1.1, 9.6, 11.03, 12.46, 13.89, 15.32, 16.75, 18.18, 20.38, 18.18, 16.75, 15.32, 13.89, 12.46, 11.03,
                 9.6, 1.1, 0]

#BR intervals

intervals_br = [[0, 562], [772, 1235], [2192, 2635], [2770, 3030], [3163, 3603], [3812, 4399], [4659, 5146], [5392, 6031],
                [6258, 6739], [7100, 7686], [7803, 7992], [8072, 8268], [8337, 8519], [8555, 8765], [8805, 9045], [9083, 9278],
                [9344, 9580], [9629, 9841], [9894, 10171]]

intervals_tr = [[0, 419], [803, 1484], [2323, 3108], [3297, 3663], [3881, 4197], [4332, 4688], [5066, 5359], [5543, 5836],
                [6090, 6482], [6618, 7429], [7692, 8177], [8392, 8720], [8884, 9213], [9279, 9636], [9822, 10122],
                [10244, 10589], [10685, 11059], [11118, 11561], [11625, 12078]]

intervals_tl = [[0, 698], [1146, 1773], [2114, 2668], [3138, 3778], [3994, 4727], [4963, 5422], [5773, 6299], [6596, 7099],
                [8000, 8541], [8765, 9651], [9969, 10319], [10568, 10892], [11039, 11333], [11491, 11825], [12110, 12571],
                [12703, 13117], [13266, 13484], [13723, 14081], [14269, 14607]]

intervals_bl = [[0, 561], [1040, 1719], [2801, 3247], [3503, 3939], [4453, 4850], [5166, 5541], [6017, 6511], [6944, 7343],
                [7886, 8458], [8661, 9410], [10637, 11515], [12028, 12343], [12717, 13221], [13456, 13922], [14169, 14672],
                [14962, 15452], [15721, 16159], [16320, 16759], [16951, 17321]]