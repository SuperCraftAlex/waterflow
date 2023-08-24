import os
import sys
import subprocess
import time
import signal
import platform

tests = []

started = 0
ok = 0
fail = 0
term = 0

for root, dirs, files in os.walk("tests/"):
  for file in files:
    path = os.path.join(root, file)

    proc = subprocess.Popen(["python3","wf/wf.py",path], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    tests.append((path, proc))
    started += 1

start = time.time()

while True:
  if len(tests) == 0:
    break
  for test in tests:
    proc = test[1]
    poll = proc.poll()
    if not proc.returncode is None:
      print("test " + test[0] + " finished " + ("succesfully" if proc.returncode == 0 else "with errors") + "!")
      if proc.returncode == 0:
        ok += 1
      else:
        fail += 1
      tests.remove(test)
  if time.time() - start > 6:
    for test in tests:
      term += 1
      print("test " + test[0] + " timed out!")
    break

print("")

ss = str(started)
print(str(ok) + " / " + ss + " tests finished succesfully")
print(str(fail) + " / " + ss + " tests failed")
print(str(term) + " / " + ss + " tests timed out")

PID = os.getpid()
if platform.system() != "Windows":
  PGID = os.getpgid(PID)
if platform.system() != "Windows":
  os.killpg(PGID, signal.SIGKILL)
else:
  os.kill(PID, signal.SIGTERM)
