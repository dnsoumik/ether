
export const ComponentList: Component[] = [
    {
        id: "input",
        label: "Input",
        expand: false,
        icon: {
            type: 'mat',
            data: 'edit'
        }
    },
    {
        id: "button",
        label: "Input",
        expand: false,
        icon: {
            type: 'mat',
            data: 'edit'
        }
    },
];


export interface Component {
    id: String,
    label: String,
    expand: boolean,
    icon: Object,
}