import sys
import extract

if len(sys.argv) < 17:
    pass
#if len(sys.argv) < 18:
    #print(
        #f"Error: Incorrect number of arguments. Expected 17, got {
            #len(
                #sys.argv) -
            #1}",
        #file=sys.stderr,
    #)
    #print(f"Usage: {sys.argv[0]} <arg1> <arg2> ... <arg17>", file=sys.stderr)
    #sys.exit(1)
else:
    extract.NEOBootMainEx(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4],
        sys.argv[5],
        sys.argv[6],
        sys.argv[7],
        sys.argv[8],
        sys.argv[9],
        sys.argv[10],
        sys.argv[11],
        sys.argv[12],
        sys.argv[13],
        sys.argv[14],
        sys.argv[15],
        sys.argv[16],
        sys.argv[17],
    )
