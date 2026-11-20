"""Trusted shipped workflow fingerprints (0.10.0, 0.10.1, 0.10.2, 0.10.3 and pre-feature source)."""
# Released 0.10.2 additions are frozen from immutable commit
# 6259a15a73b7de93b7a0388feb90c451c6cf36b6; see
# tests/fixtures/session-guidance-0.10.2/README.md for source provenance.
KNOWN = {
    # Exact released 0.10.2 retrospective; frozen fixture documents source.
    'retrospective.md': frozenset(['40405cec89c84c316fe841f92b48cd17e484359ca4edd6ed07f6ba21aedcc0f4', '5368bbecf6aea0c663ef8c4d5e7a921003026ed78a89366ff16f2a0cc1574dc4', '5c72a2ec75f1f4df145ee79678e15a421b6999a766aa24ec1d01a480e0f0c8e4', 'b2924afb8d401f90e6905ef490a762d1a1e286eac6f1c012889387df260aa8e9', 'bf52d12c9fe5c92d6f64183dc459d91ea028af0b362ff6a9adbdfb0fc576a69e', 'f8eb8354e0ad2bf4a40edcbb92b632dfc657474885100d0b218464d3ce39351f']),
    'conversation.md': frozenset(['1b0f27b5a133e65571b9d487d48611fc38fe0cef68e9d2440b1ff0d79eec6def', '5b1bf354f929bc0adf72f3f893d11f1e0a77e81b485344d25dbdbc7182173236', '99c6a23d2439bef32a6a59289c4d9cd392ee9667acca725fd6918357d624d2a2', '9be000952e7caf5edd9690ead66aadbe8ebc354cfeab63f7afed6fd7988090ac', 'dfe01a61e53b9ec8a960714baea28719fc8eaa94a1491eafd10fe1f619c361cd', 'ffc4f995460960dcc393de8c33b63b6202c0acb264db23ffc843babdf69b840c', '010118bd817f4a406e52e345a23e97c294274090d243f1aa3b91b598f1d1f7e8', '1dcba9b07d905ec4c159ec480cbff234940e3ed42559652f04138ebc1f7f9c67', '220c5c63d675728ec5ea0e753ddb9380e1c82c3431e84d181a61e24e36362e04', '3c8447d48d1a0355193fa9288fa21107889adfc31cb1db99cc92e33820ca8066', '443ba6b67bf7807bee929a344942629410259344b9226eceed2bf79a90362380', '48e6dfcf686c377d9282241619b55a4dc47145977a5774cdf8cb4596fa6ed8bb', '79d8924f0dcfc7dfcdc8728b69c53d021169cd4c2bfd07a1ef6acd2baa61692c', '8480bb4ec9d68e17d4ae63c1d38241d5d5d27a2d78c195b1a9708b9bc842c1ef', '8966d22d44c6b7344f37b9871c16147980e0fa47c5ddb2385ecd8102d71422f2', '8cf503cc7af3df2e4408c0a163a0e04c06824d9b73a2e31e4be31b9361358656', 'bd9d9a4293575544f080ebe49ee84024dc12a0ac00aabfa7141bdb41209e07b1', 'f04a1c0fd300c63f2dec7777aee4a6d9b78a027705c69ec2aec7438848eae234']),
    'debugging.md': frozenset(['150d8aa8c008b2a9b0dfa8962a7fca0410c9f8cdca06c81ab8e1463f77cd3859', '23b8ada16221ce4f08532529a79dcf6c705c436767e17855d5507f080db87388', '082637983c394396bd0448b314c1892dabce7ccdb3f3a3af140ad377ace1cad2', 'bb416e58740a67828cc3de7106ed670fc240d9d0e8caaf452dce0339cf72a1bb', 'e0720957f6296e9bbf58b8d0adedc531eb5bbd12feec00ef73605a52dfbf6ade', 'f75990d434e77809839a951dc30d2fa6d3ac16e56f6b016888f00c2d5f8a3009']),
    'help.md': frozenset(['03e1988259f6617a685bfb981bf1adecbad1e0c50891df6c4bd6a27df03a8243', '97878836cf0f0cde39d4298cb5b8b8f2b5a3929b27a31d719cec0fa768f96423', 'a7b5bdd11509c04cd4cccceb997fed23d74ed9a8d66633cbbc051c237b6e55d7', 'c12d5a57442d484573efc80de8171e87821baaa41520a7a418828b0e5903e866', 'd6542c65dbe401eeeb539019f7f75c181205f53323cf71a7efeef07ae9f6439a', 'e67b0995b540301e3200ad8d121dc60209d81bf3499399e97ee8c9e4d426d00f']),
}

# Exact released 0.10.4 notebook resources from 3a6807c, rendered for each host/skill source.
KNOWN['debugging.md'] |= frozenset({'4fbfa3bab213d418ab46f668da24b7fe203e6637739e9e7f1f49eb82a8a65e44'})
KNOWN['conversation.md'] |= frozenset({
    '27086e663b497c88ce0932021fed61cb9f0d1d619795c349eef3c3a5eecd1af5',  # Codex/project
    'c94dd6c6a9bcdf75d4d04329556da7872a5d8c8004cb3f8bb998b4fa33cfb9bf',  # Codex/plugin
    '1eedfb7aae8a2ea636ca891770fae450bbbfb02c2f04369da4ae23cd11798c97',  # Claude/project
    '89c575a9e6c20dfadc54251282e9cd624673daf5095bf565192e50c8af4c22f1',  # Claude/plugin
    'd4288ee6fe15bfd7705783518d14a56846da1b7c40054f5775ced4f55f546128',  # Both/project
    'be1819caa5a46585204a532e302e07f71db20e7cf798da90f6cc75ba65ab2a73',  # Both/plugin
})
KNOWN['help.md'] |= frozenset({
    '175a41e664ccf192359fbe1817e65e4dac4ee48541082952cee7644b5362c3b5',  # Codex/project
    '455df7fc9b2b404fe00a0e2598850a161c31d0653310c10ac6c163f58bab17fe',  # Codex/plugin
    '91a18cd1bea62ff85138ba14a9ce1120996fa2738a45777f09111fa346da95b9',  # Claude/project
    '70049f309dfaf94783b31f59be847b44ac23c8fb48fb568b4ecbf5eb98739e05',  # Claude/plugin
    '8974d0adaf1798492561625c9acab51f3eef09177c939dc0436ceb1c3b5a3a02',  # Both/project
    '01a98b25535644266ec6ec49c7d2a2b71c644cfea922ce44023fe0fcc2666a2c',  # Both/plugin
})
PREVIOUS_PROJECT_SKILLS = {
    'codex': 'a7dc6e2f38236cca032f0c3f6760d75aa06058f36b799a41a3422471a33e9448',
    'claude': '439e5dcd13b196ca0ce9e23b778ba7c82d5cda613f17bc699802219e7b782f47',
}

# Exact released 0.10.3 conversation guide rendered for each host/skill source,
# from tests/fixtures/session-guidance-0.10.3/conversation.md.
KNOWN['conversation.md'] |= frozenset({
    'd1cea99c20586a85948277cbf6822ad73b53ab35d80fe12c4029fff3670bf3a3',  # Codex/project
    '76cfc2c1819a97e9b685133156e7b62cbfb249c13a46d27b598bfeedebe09a9a',  # Codex/plugin
    'c3dda002376380371803e69f08ca6752e2c2d92adf45f761506352091eb3a419',  # Claude/project
    '7ed0ffc472683bf3e7c319f9f2e00f5cf4ca30ec7477483494a09171ac574e56',  # Claude/plugin
    '7967cd4c3620b74d1d4423f5f9b6547a8ab382906dc4d8df2942d3c42d67a383',  # Both/project
    'c2da78e087b6800a1102a8e473b6cc36f40b60b9d926ea2a0cabc6d87e402cf9',  # Both/plugin
})

# Exact released 0.10.4 retrospective guide rendered for each host/skill source.
KNOWN['retrospective.md'] |= frozenset({
    '2975c6424003fbf6b45b39822e0985c0524bdcde1a60604b07a3e37e2af9c17e',  # Codex/project
    '90b0022da5ac90023cf88023bdc76bf880c0aa5a5863c9c60f6ffcb1870f0497',  # Codex/plugin
    'b15dfe00698684bfc57ffc188e012c84ab3b91a409edeb03d635325af91c335a',  # Claude/project
    '0396fe76a5019a48cc543f4af43daab64858098f6afb39039ffec32841759cfc',  # Claude/plugin
    '21a1e90cea96115abbdbac2e94a0ab48de2f9a1b65ef6fee317a89565636cec5',  # Both/project
    'd11895243dceb40912ad4b45626114949a8e5b3f482a31927b793bf75cfdf846',  # Both/plugin
})

# v0.10.5 notebook/workflows/retrospective.md from 7e1dc48020bdf078555e5dbdf62cf5247547e7df.
KNOWN['retrospective.md'] |= frozenset({
    'df76c4ff8f41d969dcfb2fab3ddcc69f979d8b234c6ee88d5b41a59b5d261cf4',  # Codex/project
    '4af4e75519daa066caf14188a75f307dd343dd85842cc128e25dd1b6f6c9ac41',  # Codex/plugin
    '0bf419ab97fb86fa7081aa0fc64d25ef0d0cac53495319f509c500b32336b9b9',  # Claude/project
    'a68410df1e81e89554501ec88322a92595109c3ffba2dcfa67872e5d02aa8cf8',  # Claude/plugin
    '7565efb76d31b91913f68a7da6ae58fb6e28fdf09ee4248d625b7183cf93ca6c',  # Both/project
    'e256c4ee3c1242e8cf71ff98d804cbe5135bfd6082a4398de361a2cbb808cea6',  # Both/plugin
})

SESSION_BLOCKS = ("<!-- novel-creator:session-guidance:start -->\nFollow the revised [conversation and save rules](.novel-notebook/workflows/conversation.md),\n[character-development boundary](.novel-notebook/workflows/character-development.md)\nand [role ownership](.novel-notebook/workflows/agents.md). These shared rules\nclarify older general save wording: writer approval, verified file saves and\nverified local Git checkpoints are distinct. Approved but unwritten work remains\nunsaved; saved files can have a pending checkpoint. Keep character-development\ndrafts in chat until explicit save authority, including during a pending save.\nUse the host's approved scoped access route when available for an authorized\ncheckpoint, preserving unrelated staging; otherwise disclose the limitation.\nFor an explicitly requested local notebook retrospective, follow the read-only\n[debugging guide](.novel-notebook/workflows/debugging.md#local-notebook-retrospective)\non writer-selected public evidence. This adds no retrospective CLI, capture\nactivation, upload or publication authority.\n<!-- novel-creator:session-guidance:end -->", "<!-- novel-creator:session-guidance:start -->\nFollow the revised [conversation and save rules](.novel-notebook/workflows/conversation.md),\n[character-development boundary](.novel-notebook/workflows/character-development.md)\nand [role ownership](.novel-notebook/workflows/agents.md). These shared rules\nclarify older general save wording: writer approval, verified file saves and\nverified local Git checkpoints are distinct. Approved but unwritten work remains\nunsaved; saved files can have a pending checkpoint. Keep character-development\ndrafts in chat until explicit save authority, including during a pending save.\nUse the host's approved scoped access route when available for an authorized\ncheckpoint, preserving unrelated staging; otherwise disclose the limitation.\nFor a requested retrospective or active-session opt-in at explicit closure,\nfollow the [retrospective workflow](.novel-notebook/workflows/retrospective.md).\nStop known current debugging before review and keep it off. Exact outgoing\nissue/attachment approval is required before sharing; no story save or commit.\n<!-- novel-creator:session-guidance:end -->")
