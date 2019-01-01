
from DBUtility import DBUtility

class LossProcess(object):

	def __init__(self):
		self.dbUtil = DBUtility('localhost', 3306, 'root', 'Initial0')

	def getUserLoss(self):
		sql = "select * from hx.UserLoss order by UserId "
		return self.dbUtil.getQueryResult(sql)

	def countUser(self):
		sql = "select count(1) from hx.UserLoss"
		count = self.dbUtil.getQueryResult(sql)
		return count[0][0]

	def processLossForUser(self, userId, loss):
		sql = "select * from hx.ORDERS where UserId = '%s' order by buyDate desc, id desc" % userId
		orders = self.dbUtil.getQueryResult(sql)
		totalLoss = 0
		lossOrders = []
		for order in orders:
			totalLoss += order[14]
			lossOrders.append((userId, order[0]))
			if totalLoss >= loss:
				break
		values = ','.join([ "('%s', '%s')" % x for x in lossOrders])
		sql = "insert into hx.LossOrders values %s " % values
		self.dbUtil.execQuery(sql)
		return lossOrders

	def processLoss(self):
		lossOrders = []
		users = process.getUserLoss()
		n = 0
		for user in users:
			userId = user[0]
			loss = user[9]
			lossOrders.extend(process.processLossForUser(userId, loss))
			if n % 100 == 0:
				print(n)
			n += 1

if __name__ == "__main__":
	process = LossProcess()
	# process.processLossForUser('5013344', 6360750.71)
	process.processLoss()


