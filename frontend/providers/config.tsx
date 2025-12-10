export const getParamKeys = (tab: number) => {
    switch(tab) {
    case 1:
        return ['name']
    default:
        return ['query']
    }
}