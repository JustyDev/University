ClearAll["Global`*"];

outputDir = DirectoryName[$InputFileName];
If[outputDir === "", outputDir = Directory[]];

notebookPath = FileNameJoin[{outputDir, "lab2_primes.nb"}];

codeExpr = HoldComplete[
  ClearAll["Global`*"];

  primeList = {};
  candidates = {};

  Do[
    AppendTo[candidates, n];
    divisors = {};
    Do[
      If[IntegerQ[N[n/k]] && Mod[n, k] == 0, AppendTo[divisors, k]],
      {k, 2, n - 1}
    ];
    If[Complement[divisors, {}] === {} && n > 1, AppendTo[primeList, n]];
    If[Length[primeList] >= 10, Break[]],
    {n, 2, 100}
  ];

  xValues = Range[Length[primeList]];
  points = Transpose[{xValues, primeList}];

  fitModel = Fit[points, {1, x, x^2}, x];
  approxValues = Table[fitModel /. x -> i, {i, xValues}];
  errors = primeList - approxValues;

  maxError = Max[Abs[errors]];
  mse = N[Mean[errors^2]];
  mae = N[Mean[Abs[errors]]];

  combinedPlot = Show[
    ListPlot[
      points,
      Joined -> True,
      PlotStyle -> Directive[Blue, Thickness[0.006]],
      PlotMarkers -> Automatic,
      PlotLegends -> {"Prime numbers"},
      PlotLabel -> "First 10 Prime Numbers and Quadratic Approximation",
      AxesLabel -> {"Index", "Value"},
      AxesOrigin -> {1, 0},
      ImageSize -> Large
    ],
    Plot[
      fitModel,
      {x, 1, Length[primeList]},
      PlotStyle -> Directive[Red, Thickness[0.006]],
      PlotLegends -> {"Quadratic fit"},
      AxesLabel -> {"Index", "Value"},
      AxesOrigin -> {1, 0},
      ImageSize -> Large
    ],
    PlotRange -> All,
    ImagePadding -> 20
  ];

  figure1 = Show[
    combinedPlot,
    ListPlot[
      Transpose[{xValues, errors}],
      Joined -> True,
      PlotStyle -> Directive[Darker[Green], Thickness[0.006]],
      PlotMarkers -> Automatic,
      PlotLegends -> {"Approximation error"},
      AxesLabel -> {"Index", "Error"},
      AxesOrigin -> {1, 0},
      ImageSize -> Large
    ],
    PlotRange -> All,
    PlotLabel -> "Figure 1. Primes, Quadratic Approximation, and Error",
    ImagePadding -> 20
  ];

  primeList
  points
  fitModel
  approxValues
  maxError
  mse
  mae
  combinedPlot
  figure1
];

nb = Notebook[
  {
    Cell["Lab 2: Prime Numbers and Quadratic Approximation", "Title"],
    Cell[
      "Execute the input cell below. It generates the first 10 prime numbers, builds the quadratic least-squares approximation, computes Max Error, MSE, MAE, and draws the required plots.",
      "Text"
    ],
    Cell[BoxData @ ToBoxes[Defer[ReleaseHold[codeExpr]]], "Input"],
    Cell[
      TextData[{
        "Expected outputs: `primeList`, `points`, `fitModel`, `approxValues`, `maxError`, `mse`, `mae`, `combinedPlot`, `figure1`."
      }],
      "Text"
    ]
  },
  WindowTitle -> "lab2_primes",
  StyleDefinitions -> "Default.nb"
];

Put[nb, notebookPath];
Print[notebookPath];
