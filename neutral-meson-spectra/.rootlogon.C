{
	Int_t start = 10000;
	const Int_t n_colors = 13;
	Int_t colors[13][3] = {
		{219, 94, 86},
		{86, 111, 219},
		{86, 219, 127},
		{219, 194, 86},
		{86, 211, 219},
		{160, 86, 219},
		{219, 86, 178},
		{112, 174, 192},
		{133, 122, 170},
		{102, 194, 165},
		{229, 196, 148},
		{52, 73, 94},
		{153, 93, 18}
	};

	TColor * my_colors[n_colors];
	for (Int_t i = 0; i < n_colors; ++i)
		new TColor(start + i, colors[i][0]/255., colors[i][1]/255., colors[i][2]/255.);
}