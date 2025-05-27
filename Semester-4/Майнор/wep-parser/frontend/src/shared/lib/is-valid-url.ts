export const isValidUrl = (url: string): boolean => {
  const urlPattern = new RegExp(
    '^(https?:\\/\\/)?' + // протокол
    '((([^:\\/\\s]+\\.)+[a-z]{2,})|' + // доменное имя
    '((\\d{1,3}\\.){3}\\d{1,3}))' + // или IP-адрес
    '(\\:\\d+)?' + // порт
    '(\\/[-a-z\\d%@_.~+&:]*)*' + // путь
    '(\\?[;&a-z\\d%@_.,~+&:=-]*)?' + // строка запроса
    '(\\#[-a-z\\d_]*)?$', 'i' // якорь
  );
  return urlPattern.test(url);
}