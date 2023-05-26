const ts = require("typescript");

let filename = process.argv[2];
const debugAll = process.argv[3] === "--all";

console.log("debugging filename:", filename);

const program = ts.createProgram([filename], {
  // allowJs: true,
  noEmit: true,
  jsx: ts.JsxEmit.ReactJSX,
  esModuleInterop: true,
  // allowArbitraryExtensions: true,
});
const emitResult = program.emit();

let allDiagnostics = ts
  .getPreEmitDiagnostics(program)
  .concat(emitResult.diagnostics);

allDiagnostics.forEach((diagnostic, i) => {
  if (diagnostic.file) {
    const baseName = process.cwd() + "/";
    const relativeFileName = diagnostic.file.fileName.replace(baseName, "");

    if (!debugAll && relativeFileName !== filename) return;

    let { line, character } = diagnostic.file.getLineAndCharacterOfPosition(
      diagnostic.start,
    );
    let message = ts.flattenDiagnosticMessageText(
      diagnostic.messageText.replace(baseName, ""),
      "\n",
    );
    console.log(
      `Error #${i + 1} ${relativeFileName} line ${line + 1}): ${message}`,
    );
    // const lines = diagnostic.file.text.split("\n");
    // console.log(temp, line, character);
    let lineOfCode = diagnostic.file.text.split("\n")[line];
    console.log(`${line + 1}) ${lineOfCode}\n`);
  } else {
    console.log(
      `${ts.flattenDiagnosticMessageText(diagnostic.messageText, "\n")}`,
    );
  }
});
