// Pruebas del corrector integrado en el HTML, sin dependencias.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(__dirname + '/examen_patrones.html', 'utf8');
const script = html.match(/<script type="module">([\s\S]*?)<\/script>/)[1];
const core = script.split('// INTERFAZ')[0];
const context = vm.createContext({});
vm.runInContext(core, context);
function check(value, answer, numeric) {
  return vm.runInContext(`esCorrecta(${JSON.stringify(value)}, ${JSON.stringify(answer)}, ${numeric})`, context);
}
assert.equal(check('107,10', '107.1', true), true);
assert.equal(check('107.10', '107.1', true), true);
assert.equal(check('', '0', true), false);
assert.equal(check('   ', '0', true), false);
assert.equal(check('0', '0', true), true);
assert.equal(check('107.11', '107.1', true), false);
assert.equal(check('Infinity', 'Infinity', true), false);
assert.equal(check('0x10', '16', true), false);
assert.equal(check('True', 'True', false), true);
assert.equal(check('False', 'True', false), false);
assert.equal((html.match(/<section class="q"/g) || []).length, 40);
assert.equal((html.match(/data-answer=/g) || []).length, 80);
console.log('Corrector: 10 casos aprobados; 40 preguntas y 80 incisos.');
