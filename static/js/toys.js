const USE_CLASS_VERSION = true; //true -> class-extends, false -> прототипное наследование

function ToyProto(name, price) {
    this.name = name;
    this.price = price;
}

ToyProto.prototype.getName = function() { return this.name; }
ToyProto.prototype.setName = function(name) { this.name = name; }
ToyProto.prototype.getPrice = function() { return this.price; }
ToyProto.prototype.setPrice = function(price) { this.price = price; }
ToyProto.prototype.showInfo = function() {
    return `${this.name} — ${this.price} руб.`;
};

function ToyWithAgeProto(name, price, ageFrom, ageTo) {
    ToyProto.call(this, name, price);
    this.ageFrom = ageFrom;
    this.ageTo = ageTo;
}
ToyWithAgeProto.prototype = Object.create(ToyProto.prototype);
ToyWithAgeProto.prototype.constructor = ToyWithAgeProto;

ToyWithAgeProto.prototype.getAgeRange = function() {
    return `для детей от ${this.ageFrom} до ${this.ageTo} лет`;
};
ToyWithAgeProto.prototype.showInfo = function() {
    return `${this.name} — ${this.price} руб., ${this.getAgeRange()}`;
};

class ToyClass {
    constructor(name, price) {
        this.name = name;
        this.price = price;
    }
    getName() { return this.name; }
    setName(name) { this.name = name; }
    getPrice() { return this.price; }
    setPrice(price) { this.price = price; }
    showInfo() { return `${this.name} — ${this.price} руб.`; }
}

class ToyWithAgeClass extends ToyClass {
    constructor(name, price, ageFrom, ageTo) {
        super(name, price); // вызов родительского конструктора
        this.ageFrom = ageFrom;
        this.ageTo = ageTo;
    }

    getAgeRange() {
        return `для детей от ${this.ageFrom} до ${this.ageTo} лет`;
    }

    showInfo() {
        return `${this.name} — ${this.price} руб., ${this.getAgeRange()}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const toyForm = document.getElementById('toyForm');
    const toyList = document.getElementById('toyList');
    const resultDiv = document.getElementById('result');
    const showExpensiveBtn = document.getElementById('showExpensiveBtn');

    let toys = [];

    toyForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = document.getElementById('toyName').value;
        const price = parseFloat(document.getElementById('toyPrice').value);
        const ageFrom = parseInt(document.getElementById('ageFrom').value);
        const ageTo = parseInt(document.getElementById('ageTo').value);

        let toy;
        if (USE_CLASS_VERSION) {
            toy = new ToyWithAgeClass(name, price, ageFrom, ageTo);
        } else {
            toy = new ToyWithAgeProto(name, price, ageFrom, ageTo);
        }

        toys.push(toy);
        displayToys();
        toyForm.reset();
    });

    function displayToys() {
        toyList.innerHTML = '';
        toys.forEach((toy) => {
            const div = document.createElement('div');
            div.textContent = toy.showInfo();
            toyList.appendChild(div);
        });
    }

    showExpensiveBtn.addEventListener('click', () => {
        if (toys.length === 0) {
            resultDiv.textContent = 'Игрушек нет!';
            return;
        }

        const maxPrice = Math.max(...toys.map(t => t.price));
        const expensiveToys = toys.filter(t => Math.abs(maxPrice - t.price) <= 1);

        resultDiv.innerHTML = `<p>Самые дорогие игрушки (разница ≤ 1 руб.):</p>` +
            expensiveToys.map(t => `<div>${t.showInfo()}</div>`).join('');
    });
});
