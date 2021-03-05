
export const ComponentList: Component[] = [
    {
        id: "input",
        label: "Input",
        eSelect: false,
        icon: {
            type: 'mat',
            data: 'edit'
        }
    },
    {
        id: "button",
        label: "Input",
        eSelect: false,
        icon: {
            type: 'mat',
            data: 'edit'
        }
    },
];


export interface Component {
    id: String,
    label: String,
    eSelect: boolean,
    icon: Object,
}