#set page(
  paper: "a4",
  margin: (x: 1cm, top: 2cm, bottom:1.75cm),
  header: if "hsk" in sys.inputs [
    #align(center, text(size: 16pt, weight: "bold", "HSK " + sys.inputs.hsk))
  ] else [
    #align(center, text(size: 16pt, weight: "bold", "Title"))
  ],
  footer: locate(
    location => if [#calc.rem(location.page(), 2)] == [0] {
      align(right, counter(page).display("1"));
    } else {
      align(left, counter(page).display("1"));
    }
  )
)

#let worksheet(
  id,
  number,
  category,
  chinese,
  pinyin,
  english
) = {
  set block(
    width: 100%, 
    height: 100%,
  )
  
  set line(
    stroke: (
      paint: gray,
      thickness: 0.5pt,
      dash: "dash-dotted"
    )
  )

  show grid: set block(spacing: 0pt)

  block(height: auto, breakable: false)[
    // Header grid
    #grid(
      columns: (19mm, 1fr),
      rows: (7mm),
      gutter: 0mm,
      stroke: (0.75pt + black),
      align(
        center + horizon, 
        text(
          size: 12pt,
          weight: "bold", 
          id
        )
      ),
      block(
        inset: ((left: 6pt)),
        align(
          start + horizon, 
          text(pinyin)
        )
      )
    )
  
    // Body grid
    #for character in chinese {
      grid(
        columns: (19mm, 19mm, 19mm, 19mm, 19mm, 19mm, 19mm, 19mm, 19mm, 19mm),
        rows: (19mm),
        gutter: 0mm,
        stroke: (0.75pt + black),
        grid.cell(
          colspan: 1,
          block(
            stroke: (top: (2pt + white),),
            align(
              center + horizon, 
              text(
                font: "Noto Serif CJK SC",
                size: 42pt, 
                character
              )
            )
          ),
        ),
        grid.cell(
          colspan: 1,
          block(
            [
              #place(top + left, 
                line(start: (0pt, 0pt), end: (19mm, 19mm))
              )
              #place(top + left, 
                line(start: (0pt, 19mm), end: (19mm, 0pt))
              )
              #place(top + left, 
                line(start: (0pt, 9.5mm), end: (19mm, 9.5mm))
              )
              #place(top + left, 
                line(start: (9.5mm, 0pt), end: (9.5mm, 19mm))
              )
              #block(
                align(
                  center + horizon, 
                  text(
                    font: "Noto Serif CJK SC",
                    fill: gray,
                    size: 42pt, 
                    character
                  )
                )
              )
            ]
          ),
        ),
        grid.cell(
          colspan: 1,
          block(
            [
              #place(top + left, 
                line(start: (0pt, 0pt), end: (19mm, 19mm))
              )
              #place(top + left, 
                line(start: (0pt, 19mm), end: (19mm, 0pt))
              )
              #place(top + left, 
                line(start: (0pt, 9.5mm), end: (19mm, 9.5mm))
              )
              #place(top + left, 
                line(start: (9.5mm, 0pt), end: (9.5mm, 19mm))
              )
              #block(
                align(
                  center + horizon, 
                  text(
                    font: "Noto Serif CJK SC",
                    fill: silver,
                    size: 42pt, 
                    character
                  )
                )
              )
            ]
          ),
        ),
        ..for x in range(1, 8) {
          (
            grid.cell(
              colspan: 1,
              block(
                [
                  #place(top + left, 
                    line(start: (0pt, 0pt), end: (19mm, 19mm))
                  )
                  #place(top + left, 
                    line(start: (0pt, 19mm), end: (19mm, 0pt))
                  )
                  #place(top + left, 
                    line(start: (0pt, 9.5mm), end: (19mm, 9.5mm))
                  )
                  #place(top + left, 
                    line(start: (9.5mm, 0pt), end: (9.5mm, 19mm))
                  )
                ]
              ),
            ),
          )
        },
      )
    }
  
    // Footer grid
    #grid(
      columns: (19mm, 2fr, 1fr),
      rows: (7mm),
      gutter: 0mm,
      stroke: (0.75pt + black),
      block(
        stroke: (top: (2pt + white))
      ),
      block(
        inset: (left: 6pt),
        align(
          start + horizon, 
          text(english)
        )
      ),
      block(
        inset: (left: 6pt),
        align(
          start + horizon, 
          text("(" + str(int(number) + 1) + ") " + category)
        )
      )
    )
  ]
}

#let results = if "csv_file_path" in sys.inputs { 
  csv(sys.inputs.csv_file_path, delimiter: ";") 
} else {
  csv("data.csv", delimiter: ";")
}
#for (index, result) in results.enumerate() [
  #worksheet(str(index + 1), ..result)
]