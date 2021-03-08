
export class Compute {

    static lastIndex = 0;
    static getUniqueId(): number {
        this.lastIndex++;
        return this.lastIndex;
    }

}