document.addEventListener("DOMContentLoaded", function () {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const baseOptions = {
    localization: { locale: "en-GB", format: "dd/MM/yyyy", hourCycle: "h23" },
    display: {
      components: {
        decades: false, year: true, month: true, date: true,
        hours: false, minutes: false, seconds: false
      },
      placement: "bottom"
    },
    restrictions: { minDate: today },
    container: document.body,
    allowInputToggle: true
  }

  document.querySelectorAll('#start-date-picker, [id^="start-date-picker-"]').forEach(startGroup => {
    const id = startGroup.id.replace("start-date-picker-", "")
    const endGroup  = document.getElementById(`end-date-picker-${id}`)
    const startInput = document.getElementById(`start-date-${id}`)
    const endInput   = document.getElementById(`end-date-${id}`)

    if (!endGroup || !startInput || !endInput) return

    new tempusDominus.TempusDominus(startGroup, baseOptions)
    new tempusDominus.TempusDominus(endGroup, baseOptions)

    // Auto set end date = start date + 1 day
    startInput.addEventListener("change", () => {
      const [day, month, year] = startInput.value.split("/")
      const startDate = new Date(`${year}-${month}-${day}`)
      if (isNaN(startDate)) return
      const nextDate = new Date(startDate.getTime() + 86400000)
      endInput.value = `${String(nextDate.getDate()).padStart(2,"0")}/${String(nextDate.getMonth()+1).padStart(2,"0")}/${nextDate.getFullYear()}`
    })
  })
})
