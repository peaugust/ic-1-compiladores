#!/bin/bash

CLASSPATH=".:/usr/local/lib/antlr-4.9.1-complete.jar:$CLASSPATH"
antlr4() {
java -Xmx500M -cp "/usr/local/lib/antlr-4.9.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool $*
}
grun() {
java -Xmx500M -cp "/usr/local/lib/antlr-4.9.1-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig $*
}

antlr4 exemplo.g4 -o build
cd build
javac *.java
grun exemplo start -gui < ../input.txt