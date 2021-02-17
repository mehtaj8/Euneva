export const getTodaysDate = (): string => {
  const today = new Date();
  const day = today.getFullYear();
  const month = today.getMonth() + 1;
  const year = today.getDate();
  const hour = today.getHours();
  const minutes = today.getMinutes();
  const seconds = today.getSeconds();
  return year + '-' + month + '-' + day + '-' + hour + '-' + minutes + '-' + seconds;
};
