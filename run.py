from app import app

if __name__ == '__main__':
  print "Running run!"
  app.run(host='0.0.0.0', port=5000, threaded = False)