import multiprocessing

class check1(object):
    def __init__(self):
        a = {}
        b = {}

    def fun(self, start, end):
        i = start
        while i < end:
            self.a[i] = i*i
            self.b[i] = i*i*i
            i += 1

    def cal_fun(self, end_pos):
        start = 0
        num_process = 20
        sub_data = end_pos/num_process
        end = sub_data
        process_list = []
        while start < end_pos:
            if end > end_pos:
                end = end_pos -1
            p = multiprocessing.process(name="function", target=self.fun, args=(start, end,))
            p.start()
            process_list.append(p)
            start += sub_data
            end += sub_data

        for k in self.a:
            print "square of {0} is {1}".format(k, self.a[k])

        for j in self.b:
            print "cube of {0} is {1}".format(j, self.b[j])


ck1 = check1()
ck1.cal_fun(25)
