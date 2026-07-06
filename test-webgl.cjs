const fs = require('fs');

const content = fs.readFileSync('C:\\Users\\User\\.gemini\\antigravity\\brain\\8a4ec52f-20f2-4edd-890a-060a38fad5c3\\.system_generated\\steps\\327\\content.md', 'utf-8');
const scriptMatch = content.match(/function _0x4f01[\s\S]+/);

if (!scriptMatch) {
  console.log("Could not find script");
  process.exit(1);
}

const script = scriptMatch[0];

const globalScope = {
  window: {},
  document: new Proxy({}, {
    get: function(target, prop) {
      console.log('Accessed document.', prop);
      if (prop === 'referrer') return 'https://aminebarka.dev';
      if (prop === 'querySelector') return (selector) => { console.log('querySelector', selector); return null; };
      if (prop === 'querySelectorAll') return (selector) => { console.log('querySelectorAll', selector); return []; };
      if (prop === 'getElementById') return (id) => { console.log('getElementById', id); return { innerHTML: '', value: '' }; };
      if (prop === 'getElementsByTagName') return (tag) => { console.log('getElementsByTagName', tag); return []; };
      return null;
    }
  })
};

const vm = require('vm');
const context = vm.createContext(globalScope);

try {
  vm.runInContext(script, context);
} catch (e) {
  console.log("Error:", e.message);
}

console.log("window properties after script:", globalScope.window);
