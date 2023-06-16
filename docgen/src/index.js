const PizZip = require("pizzip");
const Docxtemplater = require("docxtemplater");
const expressionParser = require("docxtemplater/expressions.js");

const fs = require("fs");
const path = require("path");
const jsonObject = require("./labels.json");

// Load the docx file as binary content
const content = fs.readFileSync(
    path.resolve(__dirname, "template.docx"),
    "binary"
);

const zip = new PizZip(content);

const doc = new Docxtemplater(zip, {
    paragraphLoop: true,
    linebreaks: true,
    parser: expressionParser,
    delimiters: { start: "{{", end: "}}" }
});


// Render the document
doc.render(jsonObject);

const buf = doc.getZip().generate({
    type: "nodebuffer",
    // compression: DEFLATE adds a compression step.
    // For a 50MB output document, expect 500ms additional CPU time
    compression: "DEFLATE",
});

// buf is a nodejs Buffer, you can either write it to a
// file or res.send it with express for example.
fs.writeFileSync(path.resolve(__dirname, "CX Review Doc.docx"), buf);