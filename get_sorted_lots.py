import subprocess, os, sys
from decimal import *
import re
if len(sys.argv) < 2:
        print "Usage: %s <file> [amount to spend]" % sys.argv[0]
        sys.exit(-1)
# Get the output
output = subprocess.check_output(['ledger', '-f', sys.argv[1], 'bal', '--lots'])
# Find the break
output = output.split("--------------------")[1]
# Remove the excess
lots = []
for line in output.split('\n'):
        match = re.search("(\w+)\s+\{(.+)\} \[(.+)\]", line)
        if match:
                # This line counts
                # Figure out the commodity
                lots.append([match.group(3), match.group(1), line])

for i in sorted(lots):
        print i[2]

# If we were given an amount, find the amounts from the lots that comprise the transaction
if len(sys.argv) > 2:
        parts = sys.argv[2].split(" ")
        if len(parts) != 2:
                print "Invalid format for amount"
                sys.exit(-2)

        print ":: Lot use for %s:" % sys.argv[2]
        total = Decimal(0)
        target = Decimal(parts[0])
        for i in sorted(lots):
                fields = i[2].split(" ")
                # ensure it's the right commodity
                if i[1] != parts[1]:
                        continue
                n = Decimal(fields[0])
                if total + n <= target:
                        # add it
                        total += n
                        print "\t" + i[2]
                elif total + n > target:
                        diff = target - total
                        fields[0] = diff
                        i[2] = " ".join([str(k) for k in fields])
                        print "\t" + i[2]
                        total += diff
                        break

        # Done
        if target == total:
                print "Success!"
        else:
                print "Failed to fund transaction (" + target + " != " + total + ")"

