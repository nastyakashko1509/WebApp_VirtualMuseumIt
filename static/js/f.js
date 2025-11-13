const words = ['привет', 'мир', 'js'];

const totalLetters = words.reduce((sum, word) => sum + word.length, 0);
console.log(totalLetters);