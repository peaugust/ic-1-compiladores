#! /bin/zsh

export CLASSPATH=".:/usr/local/lib/antlr-4.9.1-complete.jar:$CLASSPATH"
alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.9.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
alias grun='java -Xmx500M -cp "/usr/local/lib/antlr-4.9.1-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'

antlr4 cmm-2020.2/cmm/parser/cmm.g4 -o build
cd build/cmm-2020.2/cmm/parser
javac *.java
grun cmm start -gui < ../../../../cmm-2020.2/input.cmm

 # Run
 ./zsh-run-antlr4.sh
