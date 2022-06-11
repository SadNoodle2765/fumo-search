
const {PythonShell} = require('python-shell')

let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            scriptPath: './python',
            args: ['SadNoodle']
        }

PythonShell.run('test.py', options, (err, result) => {
            if (err) throw err;
    
            console.log('result: ', result.toString())
        })