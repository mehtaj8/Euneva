export const getTodaysDate = () => {
    const today = new Date();
    const day = today.getFullYear();
    const month = today.getMonth() + 1;
    const year = today.getDate();
    return day + '/' + month + '/' + year;
};
