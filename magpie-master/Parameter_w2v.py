'''
循环形成词向量，用于测试词向量的性能
'''
from magpie import Magpie
import os
import keras
import matplotlib.pyplot as plt
import numpy as np

#LossHistory类，保存loss和acc
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch': [], 'epoch': []}
        self.accuracy = {'batch': [], 'epoch': []}
        self.val_loss = {'batch': [], 'epoch': []}
        self.val_acc = {'batch': [], 'epoch': []}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

        #作图
    def loss_plot(self, loss_type, dir):
        iters = range(len(self.losses[loss_type]))
        #创建一个图
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')#plt.plot(x,y)，这个将数据画成曲线
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)#设置网格形式
        plt.xticks(np.arange(0, 21, 1))
        plt.grid(axis='x', linestyle='-.')
        plt.yticks(np.arange(0, 0.1, 0.01))
        plt.grid(axis='y', linestyle='-.')
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')#给x，y轴加注释
        plt.legend(loc="upper right")#设置图例显示位置
        plt.savefig(dir)
        #plt.show()


labels = ['1111', '1112', '1113', '1114', '1115', '1116', '1117', '1118', '1121', '1122', '1123',
          '1124', '1131', '1132', '1133', '1134', '1135', '1141', '1142', '1143', '1144', '1151',
          '1152', '1153', '1154', '1211', '1212', '1213', '1214', '1215', '1216', '1217', '1218',
          '1219', '1221', '1222', '1223', '1231', '1232', '1233', '1234', '1235', '1241', '1242',
          '1243', '1251', '1311', '1312', '1313', '1314', '1321', '1322', '1323', '1331', '1332',
          '1333', '1334', '1341', '1342', '1343', '1344', '1345', '1351', '1411', '1421', '1431',
          '1441', '15', '2111', '2112', '2113', '2114', '2115', '2116', '2117', '2121', '2122', '2123',
          '2124', '2131', '2132', '2133', '2134', '2141', '2142', '2143', '2144', '2145', '2146',
          '2147', '2148', '2149', '21410', '2151', '2152', '2153', '2154', '2155', '2156', '2161',
          '2162', '2163', '2164', '2165', '2166', '2167', '2168', '2171', '2172', '2173', '2174',
          '2175', '2176', '2177', '2178', '2179', '21710', '21711', '2181', '2182', '2183', '2184',
          '2185', '2186', '2187', '2188', '2191', '2192', '2193', '2194', '2195', '2196', '221', '222',
          '223', '224', '2311', '2312', '2313', '2314', '2315', '2316', '2321', '2322', '2323', '2324',
          '24', '31', '32', '33', '34', '41', '42', '43', '51', '52', '53', '54', '55', '56', '57',
          '58', '61', '7111', '7112', '7113', '7114', '7115', '7116', '7117', '7118', '7119', '71110',
          '71111', '7121', '7122', '7123', '7124', '7125', '7126', '7127', '7128', '7129', '7131',
          '7132', '7133', '7134', '7135', '7136', '7137', '7138', '7139', '71310', '71311', '71312',
          '7141', '7142', '7151', '721', '722', '723', '724', '7311', '7312', '7313', '7314', '7315',
          '7316', '7321', '7322', '7323', '7324', '7325', '7326', '7331', '7332', '7333', '7334',
          '7335', '7336', '734', '74']

#train_dir = 'data/hep-categories'    #2200条数据存放目录
train_dir = 'C:\\data\\Railway_Passenger_Transport'    #2200条数据，以及规章文电存放目录

Success = 'Success:'
error = 'error:'

magpie = Magpie()
lossHistory =LossHistory()
for EMBEDDING_SIZE in [100, 200, 300, 400, 500]:
    try:
        for MIN_WORD_COUNT in [4, 5, 6, 7, 8]:
            for WORD2VEC_CONTEXT in [4, 5, 6, 7, 8]:
                if os.path.exists('log/'+train_dir[-3:]+'_'+str(EMBEDDING_SIZE)+'_'+str(MIN_WORD_COUNT)+'_'+str(WORD2VEC_CONTEXT) + '.txt'):
                    continue
                magpie.train_word2vec(train_dir, vec_dim=EMBEDDING_SIZE, MWC=MIN_WORD_COUNT, w2vc=WORD2VEC_CONTEXT)
                magpie.fit_scaler('C:\\magpie-master\\data\\hep-categories')
                magpie.train('C:\\magpie-master\\data\\hep-categories', labels, callbacks=[lossHistory], test_ratio=0.1,
                             epochs=20, logdir='C:\\magpie-master\\log\\' + train_dir[-3:] + '_' + str(EMBEDDING_SIZE) + '_' + str(
                                          MIN_WORD_COUNT) + '_' + str(WORD2VEC_CONTEXT) + '.txt')  # 训练，10%数据作为测试数据，20轮
                lossHistory.loss_plot('epoch',
                                      'C:\\magpie-master\\pic\\' + train_dir[-3:] + '_' + str(EMBEDDING_SIZE) + '_' + str(
                                          MIN_WORD_COUNT) + '_' + str(WORD2VEC_CONTEXT) + '.jpg')
                '''
                magpie.save_word2vec_model(
                    'C:\\magpie-master\\save\\embeddings\\' + train_dir[-3:] + '_' + str(EMBEDDING_SIZE) + '_' + str(
                        MIN_WORD_COUNT) + '_' + str(WORD2VEC_CONTEXT))
                magpie.save_scaler(
                    'C:\\magpie-master\\save\\scaler\\' + train_dir[-3:] + '_' + str(EMBEDDING_SIZE) + '_' + str(
                        MIN_WORD_COUNT) + '_' + str(WORD2VEC_CONTEXT))
                magpie.save_model(
                    'C:\\magpie-master\\save\\model\\' + train_dir[-3:] + '_' + str(EMBEDDING_SIZE) + '_' + str(
                        MIN_WORD_COUNT) + '_' + str(WORD2VEC_CONTEXT) + '.h5')
                '''
                print(
                    Success + '\n' + train_dir[-3:] + '_' + str(EMBEDDING_SIZE) + '_' + str(MIN_WORD_COUNT) + '_' + str(
                        WORD2VEC_CONTEXT) + '   Success!!!')
    except:
        print(error+'\n'+train_dir[-3:] + '_' + str(EMBEDDING_SIZE) + '_' + str(MIN_WORD_COUNT) + '_' + str(WORD2VEC_CONTEXT) + '   error!!!')
    continue   # MIN_WORD_COUNT 阈值

