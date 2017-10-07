class Queue:
    def __init__(self, queue = None):
        if type(queue) is type([]):
            self.queue = queue
        elif queue is None:
            self.queue = []
        else:
            raise TypeError

    def enqueue(self, e):
        self.queue.append(e)
        return self.queue

    def dequeue(self):
        if len(self.queue) == 0:
            return None
        data = self.queue[0]     
        del self.queue[0]     
        return data
